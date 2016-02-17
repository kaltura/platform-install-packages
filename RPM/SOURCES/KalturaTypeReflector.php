<?php
/**
 * This class is used to reflect specific Kaltura objects, arrays & enums
 * This will be the place to boost performance by caching the reflection results to memcache or the filesystem
 *  
 * @package api
 * @subpackage v3
 */
class KalturaTypeReflector
{
	static private $propertyReservedWords = array(
		'objectType',
	);
	
	static private $_classMap = array();
	static private $_classInheritMap = array();
	static private $_classInheritMapLocation = "";
	
	/**
	 * @var string
	 */
	private $_type;
	
	/**
	 * @var array<KalturaPropertyInfo>
	 */
	private $_properties;
	
	/**
	 * @var array<KalturaPropertyInfo>
	 */
	private $_currentProperties;
	
	/**
	 * @var array<KalturaPropertyInfo>
	 */
	private $_constants;
	
	/**
	 * @var array<string>
	 */
	private $_constantsValues;
	
	/**
	 * @var string
	 */
	private $_description;
	
	/**
	 * @var bool
	 */
	private $_deprecated = false;
	
	/**
	 * @var bool
	 */
	private $_serverOnly = false;
	
	/**
	 * @var string
	 */
	private $_package;
	
	/**
	 * @var string
	 */
	private $_subpackage;
	
	/**
	 * @var bool
	 */
	private $_abstract = false;
	
	
	private $_permissions = array();
	
	private $_comments = null;
	
	/**
	 * Contructs new type reflector instance
	 *
	 * @param string $type
	 * @return KalturaTypeReflector
	 */
	public function KalturaTypeReflector($type)
	{
//		KalturaLog::debug("Reflecting type [$type]");
		
		if (!class_exists($type))
			throw new KalturaReflectionException("Type \"".$type."\" not found");
			
		$this->_type = $type;
		
	    $reflectClass = new ReflectionClass($this->_type);
	    $this->_abstract = $reflectClass->isAbstract();
	    $comments = $reflectClass->getDocComment();
	    if($comments)
	    {
	    	$this->_comments = $comments;
	    	$commentsParser = new KalturaDocCommentParser($comments);
	    	$this->_description = $commentsParser->description;
	    	$this->_deprecated = $commentsParser->deprecated;
	    	$this->_serverOnly = $commentsParser->serverOnly;
	    	$this->_package = $commentsParser->package;
	    	$this->_subpackage = $commentsParser->subpackage;
	    	if (!is_null($commentsParser->permissions)) {
	    		$this->_permissions = explode(',',trim($commentsParser->permissions));
	    	}
	    }
	}
	
	/**
	 * Returns the type of the reflected class
	 *
	 * @return string
	 */
	public function getType()
	{
		return $this->_type;
	}
	
	/**
	 * Return property by name 
	 * @param string $name
	 * @return KalturaPropertyInfo
	 */
	public function getProperty($name)
	{
		if ($this->_properties === null)
			$this->getProperties();
			
		if(!isset($this->_properties[$name]))
			return null;
			
		return $this->_properties[$name];
	}
	
	/**
	 * Return the type properties 
	 *
	 * @return array<KalturaPropertyInfo>
	 */
	public function getProperties()
	{
		if ($this->_properties === null)
		{
			$this->_properties = array();
			$this->_currentProperties = array();

			if (!$this->isEnum() && !$this->isArray())
			{
				$reflectClass = new ReflectionClass($this->_type);
				$classesHierarchy = array();
				$classesHierarchy[] = $reflectClass;
				$parentClass = $reflectClass;
				
				// lets get the class hierarchy so we could order the properties in the right order
				while($parentClass = $parentClass->getParentClass())
				{
					$classesHierarchy[] = $parentClass;
				}
				
				// reverse the hierarchy, top class properties should be first 
				$classesHierarchy = array_reverse($classesHierarchy);
				foreach($classesHierarchy as $currentReflectClass)
				{
					$properties = $currentReflectClass->getProperties(ReflectionProperty::IS_PUBLIC);
					foreach($properties as $property)
					{
						if ($property->getDeclaringClass() == $currentReflectClass) // only properties defined in the current class, ignore the inherited
						{
							$name = $property->name;
							if(in_array($name, self::$propertyReservedWords))
								throw new Exception("Property name [$name] is a reserved word in type [$currentReflectClass]");
								
							$docComment = $property->getDocComment();
							
							$parsedDocComment = new KalturaDocCommentParser( $docComment );
							if ($parsedDocComment->varType)
							{
								$prop = new KalturaPropertyInfo($parsedDocComment->varType, $name);
								
								$prop->setReadOnly($parsedDocComment->readOnly);
								$prop->setInsertOnly($parsedDocComment->insertOnly);
								$prop->setWriteOnly($parsedDocComment->writeOnly);
								$prop->setDynamicType($parsedDocComment->dynamicType);
								$prop->setServerOnly($parsedDocComment->serverOnly);
								$prop->setDeprecated($parsedDocComment->deprecated);
								$prop->setDeprecationMessage($parsedDocComment->deprecationMessage);
								
								$this->_properties[$name] = $prop;
								
								if ($property->getDeclaringClass() == $reflectClass) // store current class properties
								{
								     $this->_currentProperties[] = $prop;   
								}
							}
							
							if ($parsedDocComment->description)
								$prop->setDescription($parsedDocComment->description);
								
							if ($parsedDocComment->filter)
								$prop->setFilters($parsedDocComment->filter);
								
							if ($parsedDocComment->permissions)
								$prop->setPermissions($parsedDocComment->permissions);
							
							if(array_key_exists("", $parsedDocComment->validateConstraints)) 
								$prop->setConstraints($parsedDocComment->validateConstraints[""]);
							
						}
					}
				}
				
				$reflectClass = null;
			}
		} 
		
		return $this->_properties;
	}
	
	/**
	 * Return the number of inheritance generations since KalturaObject
	 *
	 * @return int
	 */
	public function getInheritanceLevel()
	{
		if($this->_type == 'KalturaObject')
			return 0;
			
		if($this->isEnum() || $this->isStringEnum())
			return 1;
			
		$parentTypeReflector = $this->getParentTypeReflector();
		if(!$parentTypeReflector)
			return 1;
			
		return $parentTypeReflector->getInheritanceLevel() + 1;
	}
	
	/**
	
	 * Return a type reflector for the parent class (null if none) 
	 *
	 * @return KalturaTypeReflector
	 */
	public function getParentTypeReflector()
	{
		if($this->_type == 'KalturaObject')
			return null;
			
	    $reflectClass = new ReflectionClass($this->_type);
	    $parentClass = $reflectClass->getParentClass();
	    if (!$parentClass)
	    	throw new Exception("API object [$this->_type] must have parent type, package: [$this->_package] subpackage [$this->_subpackage]");
	    	
	    $parentClassName = $parentClass->getName();
	    if (!in_array($parentClassName, array("KalturaObject", "KalturaEnum", "KalturaStringEnum", "KalturaTypedArray"))) // from the api point of view, those objects are ignored
            return KalturaTypeReflectorCacher::get($parentClass->getName());
	    else
	        return null;
	}
	
	/**
	 * Return a array of all sub classes names 
	 *
	 * @return array
	 */
	public function getSubTypesNames()
	{
		return self::getSubClasses($this->_type);
	}
	
	/**
	 * Return only the properties defined in the current class
	 *
	 * @return array<KalturaPropertyInfo>
	 */
	public function getCurrentProperties()
	{
		if ($this->_currentProperties === null)
		{
		    $this->getProperties();
		}
		
		return $this->_currentProperties;
	}
	
	/**
	 * returns the name of the constant according to its value 
	 *
	 * @param mixed $value
	 * @return string
	 */
	public function getConstantName($value)
	{
		if (!$this->isEnum() && !$this->isStringEnum())
			return false;
			
		$this->getConstantsValues();
		
		return array_search($value, $this->_constantsValues, false);
	}
	
	/**
	 * returns the value of the constant according to its name 
	 *
	 * @param string $name
	 * @return mixed
	 */
	public function getConstantValue($name)
	{
		if (!$this->isEnum() && !$this->isStringEnum())
			return false;
			
		$this->getConstantsValues();
		
		return (isset($this->_constantsValues[$name]) ? $this->_constantsValues[$name] : null);
	}
	
	/**
	 * Returns the enum constants
	 *
	 * @return array<string>
	 */
	public function getConstantsValues()
	{
		if (!is_null($this->_constantsValues))
			return $this->_constantsValues;
			
		$this->_constantsValues = array();
			
		if ($this->isEnum() || $this->isStringEnum())
		{
			$reflectClass = new ReflectionClass($this->_type);
			$this->_constantsValues = $reflectClass->getConstants();
		}
		
		if($this->isDynamicEnum())
		{
			$type = $this->getType();
			/* @var $type KalturaDynamicEnum */
			$baseEnumName = $type::getEnumClass();
			$pluginInstances = KalturaPluginManager::getPluginInstances('IKalturaEnumerator');
			foreach($pluginInstances as $pluginInstance)
			{
				/* @var $pluginInstance IKalturaEnumerator */
				$pluginName = $pluginInstance->getPluginName();
				$enums = $pluginInstance->getEnums($baseEnumName);
				foreach($enums as $enum)
				{
					/* @var $enum IKalturaPluginEnum */
					$enumConstans = $enum::getAdditionalValues();
					foreach($enumConstans as $name => $value)
						$this->_constantsValues[$name] = $pluginName . IKalturaEnumerator::PLUGIN_VALUE_DELIMITER . $value;
				}
			}
		}
		
		return $this->_constantsValues;
	}
	
	/**
	 * Returns the enum constants
	 *
	 * @return array<KalturaPropertyInfo>
	 */
	public function getConstants()
	{
		if (!is_null($this->_constants))
			return $this->_constants;
			
		$this->_constants = array();
		$constantsDescription = array();
		
		if ($this->isEnum() || $this->isStringEnum())
		{
			$reflectClass = new ReflectionClass($this->_type);
			$constantsDescription = call_user_func(array($this->_type, 'getDescriptions'));
			$contants = $reflectClass->getConstants();
			foreach($contants as $enum => $value)
			{
				if ($this->isEnum())
					$prop = new KalturaPropertyInfo("int", $enum);
				else
					$prop = new KalturaPropertyInfo("string", $enum);
					
				if (isset($constantsDescription[$value]))
					$prop->setDescription($constantsDescription[$value]);
				
				$prop->setDefaultValue($value);
				$this->_constants[] = $prop;
			}
		}
		
		if($this->isDynamicEnum())
		{
			$type = $this->getType();
			$baseEnumName = $type::getEnumClass();
			$pluginInstances = KalturaPluginManager::getPluginInstances('IKalturaEnumerator');
			foreach($pluginInstances as $pluginInstance)
			{
				$pluginName = $pluginInstance->getPluginName();
				$enums = $pluginInstance->getEnums($baseEnumName);
				foreach($enums as $enum)
				{
					$enumConstans = $enum::getAdditionalValues();
					foreach($enumConstans as $name => $value)
					{
						$value = $pluginName . IKalturaEnumerator::PLUGIN_VALUE_DELIMITER . $value;
						$prop = new KalturaPropertyInfo("string", $name);
						$prop->setDefaultValue($value);
							
						if (isset($constantsDescription[$value]))
							$prop->setDescription($constantsDescription[$value]);
						
						$this->_constants[] = $prop;
					}
				}
			}
		}
		
		return $this->_constants;
	}
	
	/**
	 * Returns true when the type is (for what we know) an enum
	 *
	 * @return boolean
	 */
	public function isEnum()
	{
		return is_subclass_of($this->_type, 'KalturaEnum'); 
	}
	
	/**
	 * Returns true when the type is depracated
	 *
	 * @return boolean
	 */
	public function isDeprecated()
	{
		return $this->_deprecated; 
	}
	
	/**
	 * Returns true when the type should not be generated in client libraries
	 *
	 * @return boolean
	 */
	public function isServerOnly()
	{
		return $this->_serverOnly; 
	}
	
	/**
	 * Returns true when the type is abstract
	 *
	 * @return boolean
	 */
	public function isAbstract()
	{
		return $this->_abstract; 
	}
	
	/**
	 * Returns true when the type is a filter
	 *
	 * @return boolean
	 */
	public function isFilter()
	{
		return is_subclass_of($this->_type, 'KalturaFilter');
	}
	
	/**
	 * Returns true when the type is a string enum
	 *
	 * @return boolean
	 */
	public function isStringEnum()
	{
		return is_subclass_of($this->_type, 'KalturaStringEnum');
	}
	
	/**
	 * Returns true when the type is a dynamic enum
	 *
	 * @return boolean
	 */
	public function isDynamicEnum()
	{
		return is_subclass_of($this->_type, 'KalturaDynamicEnum');
	}
	
	/**
	 * Returns true when the type is (for what we know) an array
	 *
	 * @return boolean
	 */
	public function isArray()
	{
		return is_subclass_of($this->_type, 'KalturaTypedArray');
	}
	
	/**
	 * Returns true when the type is (for what we know) an associative array
	 *
	 * @return boolean
	 */
	public function isAssociativeArray()
	{
		return is_subclass_of($this->_type, 'KalturaAssociativeArray');
	}
	
	/**
	 * When reflecting an array, returns the type of the array as string
	 *
	 * @return string
	 */
	public function getArrayType()
	{
		if ($this->isArray() && !$this->isAbstract())
		{
			$instance = new $this->_type();
			return $instance->getType(); 
		}
		
		return null;
	}
	
	public function setDescription($desc)
	{
		$this->_description = $desc;
	}
	
	public function getDescription()
	{
		return $this->_description;
	}	
	
	/**
	 * Checks whether the enum value is valid for the reflected enum 
	 *
	 * @param mixed $value
	 * @return boolean
	 */
	public function checkEnumValue($value)
	{
		if (!$this->isEnum())
			return false;
			
		$this->getConstantsValues();
		return in_array($value, $this->_constantsValues);
	}
	
	/**
	 * Checks whether the string enum value is valid for the reflected string enum 
	 *
	 * @param mixed $value
	 * @return boolean
	 */
	public function checkStringEnumValue($value)
	{
		if (!$this->isStringEnum())
			return false;
			
		$this->getConstantsValues();
		return in_array($value, $this->_constantsValues);
	}
	
	/**
	 * @param string $class
	 * @return boolean
	 */
	public function isParentOf($class)
	{
	    if (!class_exists($class))
	        return false;
	        
	    $possibleReflectionClass = new ReflectionClass($class);
        return $possibleReflectionClass->isSubclassOf(new ReflectionClass($this->_type));
	}
	
	public function isFilterable()
	{
		$reflectionClass = new ReflectionClass($this->_type);
		return $reflectionClass->implementsInterface("IFilterable");
	}
	
	public function isRelatedFilterable()
	{
		return is_subclass_of($this->_type, 'IRelatedFilterable');
	}
	
	/**
	 * @return string plugin name
	 */
	public function getPlugin()
	{
		if(!is_string($this->_package))
			return null;
			
		$packages = explode('.', $this->_package, 2);
		if(count($packages) != 2 || $packages[0] != 'plugins')
			return null;
			
		return $packages[1];
	}
	
	/**
	 * @return string package
	 */
	public function getPackage()
	{
		return $this->_package;
	}

	/**
	 * @return string subpackage
	 */
	public function getSubpackage()
	{
		return $this->_subpackage;
	}

	public function getInstance()
	{
		if($this->isAbstract())
			throw new Exception("Object type [$this->_type] is abstract and can't be instantiated");
			
		return new $this->_type;
	}
	
	public function __sleep()
	{
		if ($this->_properties === null)
			$this->getProperties();
			
		if ($this->_constants === null)
			$this->getConstants();
			
		if ($this->_constantsValues === null)
			$this->getConstantsValues();
		
		return array("_type", "_properties", "_currentProperties", "_constants", "_constantsValues", "_description", "_abstract", "_comments", "_permissions", "_subpackage", "_package", "_serverOnly", "_deprecated");
	}


	/**
	 * Set the class inherit map cache file path
	 * 
	 * @param string $path
	 */
	static function setClassInheritMapPath($path)
	{
		self::$_classInheritMapLocation = $path;
	}
	
	/**
	 * @return bool
	 */
	static function hasClassInheritMapCache()
	{
		return file_exists(self::$_classInheritMapLocation);
	}
	
	/**
	 * Set the class map array
	 * 
	 * @param array $map
	 */
	static function setClassMap(array $map)
	{
		self::$_classMap = $map;
	}
	
	protected static function loadSubClassesMap()
	{
		self::$_classInheritMap = array();
	
		if (!file_exists(self::$_classInheritMapLocation))
		{
			foreach(self::$_classMap as $class)
			{
				if(!class_exists($class))
					continue;
					
				$parentClass = get_parent_class($class);
				while($parentClass)
				{
					if(!isset(self::$_classInheritMap[$parentClass]))
						self::$_classInheritMap[$parentClass] = array();
						
					self::$_classInheritMap[$parentClass][] = $class;
					
					$parentClass = get_parent_class($parentClass);
				}
			}
			
			file_put_contents(self::$_classInheritMapLocation, serialize(self::$_classInheritMap));
		}
		else 
		{
			self::$_classInheritMap = unserialize(file_get_contents(self::$_classInheritMapLocation));
		}
	}
	
	public static function getSubClasses($class) 
	{
		if(!count(self::$_classInheritMap))
			self::loadSubClassesMap();
			
		if(isset(self::$_classInheritMap[$class]))
			return self::$_classInheritMap[$class];
			
		return array();
	}
	
	public function requiresReadPermission()
	{
		return in_array(KalturaPropertyInfo::READ_PERMISSION_NAME, $this->_permissions);
	}
	
	public function requiresUpdatePermission()
	{
		return in_array(KalturaPropertyInfo::UPDATE_PERMISSION_NAME, $this->_permissions);
	}
	
	public function requiresInsertPermission()
	{
		return in_array(KalturaPropertyInfo::INSERT_PERMISSION_NAME, $this->_permissions);
	}
	
	public function requiresUsagePermission()
	{
		return in_array(KalturaPropertyInfo::ALL_PERMISSION_NAME, $this->_permissions);
	}
}
