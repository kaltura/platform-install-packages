<?php
/**
 * Subclass for performing query and update operations on the 'kuser' table.
 *
 * 
 *
 * @package Core
 * @subpackage model
 */ 
class kuserPeer extends BasekuserPeer implements IRelatedObjectPeer
{	
	const KALTURA_NEW_USER_EMAIL = 120;
	const KALTURA_NEW_EXISTING_USER_EMAIL = 121;
	const KALTURA_NEW_USER_EMAIL_TO_ADMINS = 122;
	const KALTURA_NEW_USER_ADMIN_CONSOLE_EMAIL = 123;
	const KALTURA_NEW_EXISTING_USER_ADMIN_CONSOLE_EMAIL = 124;
	const KALTURA_NEW_USER_ADMIN_CONSOLE_EMAIL_TO_ADMINS = 125;
	
	private static $s_default_count_limit = 301;

	public static function setDefaultCriteriaFilter ()
	{
		if ( self::$s_criteria_filter == null )
		{
			self::$s_criteria_filter = new criteriaFilter ();
		}
		
		$c = KalturaCriteria::create(kuserPeer::OM_CLASS);
		$c->addAnd ( kuserPeer::STATUS, KuserStatus::DELETED, KalturaCriteria::NOT_EQUAL);
		self::$s_criteria_filter->setFilter ( $c );
	}
	
	public static function getKuserByScreenName( $screen_name  )
	{
		$c = new Criteria();
		$c->add ( kuserPeer::SCREEN_NAME , $screen_name );
		return self::doSelectOne( $c ); 
	}
	
	/**
	 * @param int $partnerId
	 * @param string $puserId
	 * @param bool $ignore_puser_kuser
	 * @return kuser
	 */
	public static function getKuserByPartnerAndUid($partnerId, $puserId, $ignorePuserKuser = false)
	{
		if(!$ignorePuserKuser && !kCurrentContext::isApiV3Context())
		{
			$puserKuser = PuserKuserPeer::retrieveByPartnerAndUid($partnerId, 0, $puserId, true);
			if($puserKuser)
				return $puserKuser->getKuser();
		}
		
		$c = new Criteria();
		$c->add(self::PARTNER_ID, $partnerId);
		$c->add(self::PUSER_ID, $puserId);

		// in case of more than one deleted kusers - get the last one
		$c->addDescendingOrderByColumn(kuserPeer::UPDATED_AT);

		return self::doSelectOne($c);
	}
	
	/**
	 * @param int $partner_id
	 * @param array $puser_ids
	 * @return array<kuser>
	 */
	public static function getKuserByPartnerAndUids($partner_id, array $puser_ids)
	{
		$c = new Criteria();
		$c->add(self::PARTNER_ID, $partner_id);
		$c->add(self::PUSER_ID, $puser_ids, Criteria::IN);
		return self::doSelect($c);
	}
	
	public static function getActiveKuserByPartnerAndUid($partner_id , $puser_id)
	{
		if ($puser_id == '')
			return null;
			
		$c = new Criteria();
		$c->add(self::STATUS, KuserStatus::ACTIVE);
		$c->add(self::PARTNER_ID, $partner_id);
		$c->add(self::PUSER_ID, $puser_id);
		return self::doSelectOne($c);			
	}
	
	public static function createKuserForPartner($partner_id, $puser_id, $is_admin = false)
	{
		
		$kuser = kuserPeer::getKuserForPartner($partner_id, $puser_id);
		
		if (!$kuser)
		{
			$lockKey = "user_add_" . $partner_id . $puser_id;
			return kLock::runLocked($lockKey, 'kuserPeer::createNewUser', array($partner_id, $puser_id, $is_admin));
		}
		return $kuser;
	}
	
	public static function createNewUser($partner_id, $puser_id, $is_admin)
	{
		$kuser = new kuser();
		$kuser->setPuserId($puser_id);
		$kuser->setScreenName($puser_id);
		$kuser->setFirstName($puser_id);
		$kuser->setPartnerId($partner_id);
		$kuser->setStatus(KuserStatus::ACTIVE);
		$kuser->setIsAdmin($is_admin);
		$kuser->save();
		return $kuser;
	}

	/**
	 * Replaces 'getKuserByPartnerAndUid' and doesn't use its default conditions.
	 * @param string $partnerId
	 * @param string $puserId
	 */
	protected static function getKuserForPartner($partnerId, $puserId) {
		self::setUseCriteriaFilter(false);
		$c = new Criteria();
		$c->add(self::PARTNER_ID, $partnerId);
		$c->add(self::PUSER_ID, $puserId);
		$c->addAnd ( kuserPeer::STATUS, KuserStatus::DELETED, KalturaCriteria::NOT_EQUAL);
		
		$kuser = self::doSelectOne($c);
		self::setUseCriteriaFilter(true);
		return $kuser;
	}
	
	/**
	 * This function returns a pager object holding the given user's favorite users
	 *
	 * @param int $kuserId = the requested user
	 * @param int $privacy = the privacy filter
	 * @param int $pageSize = number of kshows in each page
	 * @param int $page = the requested page
	 * @return the pager object
	 */
	public static function getUserFavorites($kuserId, $privacy, $pageSize, $page)
	{
		$c = new Criteria();
		$c->addJoin(kuserPeer::ID, favoritePeer::SUBJECT_ID, Criteria::INNER_JOIN);
		$c->add(favoritePeer::KUSER_ID, $kuserId);
		$c->add(favoritePeer::SUBJECT_TYPE, favorite::SUBJECT_TYPE_USER);
		$c->add(favoritePeer::PRIVACY, $privacy);
		$c->setDistinct();
		
		// our assumption is that a request for private favorites should include public ones too 
		if( $privacy == favorite::PRIVACY_TYPE_USER ) 
		{
			$c->addOr( favoritePeer::PRIVACY, favorite::PRIVACY_TYPE_WORLD );
		}
			
		$c->addAscendingOrderByColumn(kuserPeer::SCREEN_NAME);
		
	    $pager = new sfPropelPager('kuser', $pageSize);
	    $pager->setCriteria($c);
	    $pager->setPage($page);
	    $pager->init();
			    
	    return $pager;
	}

	/**
	 * This function returns a pager object holding the given user's favorite entries
	 * each entry holds the kuser object of its host.
	 *
	 * @param int $kuserId = the requested user
	 * @param int $privacy = the privacy filter
	 * @param int $pageSize = number of kshows in each page
	 * @param int $page = the requested page
	 * @return the pager object
	 */
	public static function getUserFans($kuserId, $privacy, $pageSize, $page)
	{
		$c = new Criteria();
		$c->addJoin(kuserPeer::ID, favoritePeer::KUSER_ID, Criteria::INNER_JOIN);
		$c->add(favoritePeer::SUBJECT_ID, $kuserId);
		$c->add(favoritePeer::SUBJECT_TYPE, favorite::SUBJECT_TYPE_USER);
		$c->add(favoritePeer::PRIVACY, $privacy);
		
		$c->setDistinct();
		
		// our assumption is that a request for private favorites should include public ones too 
		if( $privacy == favorite::PRIVACY_TYPE_USER ) 
		{
			$c->addOr( favoritePeer::PRIVACY, favorite::PRIVACY_TYPE_WORLD );
		}
			
		$c->addAscendingOrderByColumn(kuserPeer::SCREEN_NAME);
		
	    $pager = new sfPropelPager('kuser', $pageSize);
	    $pager->setCriteria($c);
	    $pager->setPage($page);
	    $pager->init();
			    
	    return $pager;
	}
	
	/**
	 * This function returns a pager object holding the specified list of user favorites, 
	 * sorted by a given sort order.
	 * the $mine_flag param decides if to return favorite people or fans
	 */
	public static function getUserFavoritesOrderedPager( $order, $pageSize, $page, $kuserId, $mine_flag )
	{
		$c = new Criteria();
		
		if ( $mine_flag ) 
		{
			$c->addJoin(kuserPeer::ID, favoritePeer::SUBJECT_ID, Criteria::INNER_JOIN);
			$c->add(favoritePeer::KUSER_ID, $kuserId); 
		}
		else 
		{
			$c->addJoin(kuserPeer::ID, favoritePeer::KUSER_ID, Criteria::INNER_JOIN);
			$c->add(favoritePeer::SUBJECT_ID, $kuserId); 
		}
			
		$c->add(favoritePeer::SUBJECT_TYPE, favorite::SUBJECT_TYPE_USER);
		
		// TODO: take privacy into account
		$privacy = favorite::PRIVACY_TYPE_USER;
		$c->add(favoritePeer::PRIVACY, $privacy);
		// our assumption is that a request for private favorites should include public ones too 
		if( $privacy == favorite::PRIVACY_TYPE_USER ) 
		{
			$c->addOr( favoritePeer::PRIVACY, favorite::PRIVACY_TYPE_WORLD );
		}
			
		switch( $order )
		{
			
			case kuser::KUSER_SORT_MOST_VIEWED: $c->addDescendingOrderByColumn(kuserPeer::VIEWS);  break;
			case kuser::KUSER_SORT_MOST_RECENT: $c->addAscendingOrderByColumn(kuserPeer::CREATED_AT);  break;
			case kuser::KUSER_SORT_NAME: $c->addAscendingOrderByColumn(kuserPeer::SCREEN_NAME); break;
			case kuser::KUSER_SORT_AGE: $c->addAscendingOrderByColumn(kuserPeer::DATE_OF_BIRTH); break;
			case kuser::KUSER_SORT_COUNTRY: $c->addAscendingOrderByColumn(kuserPeer::COUNTRY); break;
			case kuser::KUSER_SORT_CITY: $c->addAscendingOrderByColumn(kuserPeer::CITY); break;
			case kuser::KUSER_SORT_GENDER: $c->addAscendingOrderByColumn(kuserPeer::GENDER); break;		
			case kuser::KUSER_SORT_PRODUCED_KSHOWS: $c->addDescendingOrderByColumn(kuserPeer::PRODUCED_KSHOWS); break;
			
			default: $c->addAscendingOrderByColumn(kuserPeer::SCREEN_NAME);
		}
		
		$c->setDistinct();
		
		
	    $pager = new sfPropelPager('kuser', $pageSize);
	    $pager->setCriteria($c);
	    $pager->setPage($page);
	    $pager->init();
			    
	    return $pager;
	}
	
	
	/**
	 * This function returns a pager object holding all the users
	 */
	public static function getAllUsersOrderedPager( $order, $pageSize, $page )
	{
		$c = new Criteria();
		
		switch( $order )
		{
			
			case kuser::KUSER_SORT_MOST_VIEWED: $c->addDescendingOrderByColumn(kuserPeer::VIEWS);  break;
			case kuser::KUSER_SORT_MOST_RECENT: $c->addAscendingOrderByColumn(kuserPeer::CREATED_AT);  break;
			case kuser::KUSER_SORT_NAME: $c->addAscendingOrderByColumn(kuserPeer::SCREEN_NAME); break;
			case kuser::KUSER_SORT_AGE: $c->addAscendingOrderByColumn(kuserPeer::DATE_OF_BIRTH); break;
			case kuser::KUSER_SORT_COUNTRY: $c->addAscendingOrderByColumn(kuserPeer::COUNTRY); break;
			case kuser::KUSER_SORT_CITY: $c->addAscendingOrderByColumn(kuserPeer::CITY); break;
			case kuser::KUSER_SORT_GENDER: $c->addAscendingOrderByColumn(kuserPeer::GENDER); break;		
			case kuser::KUSER_SORT_MOST_ENTRIES: $c->addDescendingOrderByColumn(kuserPeer::ENTRIES); break;		
			case kuser::KUSER_SORT_MOST_FANS: $c->addDescendingOrderByColumn(kuserPeer::FANS); break;		
			
			default: $c->addAscendingOrderByColumn(kuserPeer::SCREEN_NAME);
		}
		
		$pager = new sfPropelPager('kuser', $pageSize);
	    $pager->setCriteria($c);
	    $pager->setPage($page);
	    $pager->init();
			    
	    return $pager;
	}
	

	public static function selectIdsForCriteria ( Criteria $c )
	{
		$c->addSelectColumn(self::ID);
		$rs = self::doSelectStmt($c);
		$id_list = Array();
		
		while($rs->next())
		{
			$id_list[] = $rs->getInt(1);
		}
		
		$rs->close();
		
		return $id_list;
	}

	public static function doCountWithLimit (Criteria $criteria, $distinct = false, $con = null)
	{
		$criteria = clone $criteria;
		$criteria->clearSelectColumns()->clearOrderByColumns();
		if ($distinct || in_array(Criteria::DISTINCT, $criteria->getSelectModifiers())) {
			$criteria->addSelectColumn("DISTINCT ".self::ID);
		} else {
			$criteria->addSelectColumn(self::ID);
		}

		$criteria->setLimit( self::$s_default_count_limit );
		
		$rs = self::doSelectStmt($criteria, $con);
		$count = 0;
		while($rs->next())
			$count++;
	
		return $count;
	}
	
	/**
	 * @param Criteria $criteria
	 * @param PropelPDO $con
	 */
	public static function doSelect(Criteria $criteria, PropelPDO $con = null)
	{
		$c = clone $criteria;
		
		if($c instanceof KalturaCriteria)
		{ 
			$c->applyFilters();
			$criteria->setRecordsCount($c->getRecordsCount());
		}

		return parent::doSelect($c, $con);
	}
	
	
	public static function doStubCount (Criteria $criteria, $distinct = false, $con = null)
	{
		return 0;
	}
	
	/**
	 * @param string $email
	 * @return kuser
	 */
	public static function getKuserByEmail($email, $partnerId = null)
	{
		$c = new Criteria();
		$c->add (kuserPeer::EMAIL, $email);
		
		if(!is_null($partnerId))
			$c->add (kuserPeer::PARTNER_ID, $partnerId);
			
		$kuser = kuserPeer::doSelectOne( $c );
		
		return $kuser;
		
	}
	
	/**
	 * @param int $id
	 * @return string
	 */
	public static function getEmailById($id)
	{
		$kuser = kuserPeer::retrieveByPK($id);
		return $kuser->getEmail();
	}

	/**
	 * @param string $email
	 * @param string $password
	 * @param int $partnerId
	 * @return kuser
	 */
	public static function userLogin($puserId, $password, $partnerId)
	{
		$kuser = self::getKuserByPartnerAndUid($partnerId , $puserId);
		if (!$kuser) {
			throw new kUserException('', kUserException::USER_NOT_FOUND);
		}

		if (!$kuser->getLoginDataId()) {
			throw new kUserException('', kUserException::LOGIN_DATA_NOT_FOUND);
		}
		
		$kuser = UserLoginDataPeer::userLoginByDataId($kuser->getLoginDataId(), $password, $partnerId);
					
		return $kuser;
	}
	
	
	public static function getByLoginDataAndPartner($loginDataId, $partnerId)
	{
		$c = new Criteria();
		$c->addAnd(kuserPeer::LOGIN_DATA_ID, $loginDataId);
		$c->addAnd(kuserPeer::PARTNER_ID, $partnerId);
		$c->addAnd(kuserPeer::STATUS, KuserStatus::DELETED, Criteria::NOT_EQUAL);
		$kuser = self::doSelectOne($c);
		if (!$kuser) {
			return false;
		}
		return $kuser;
	}
	
	
	/**
	 * Adds a new kuser and user_login_data records as needed
	 * @param kuser $user
	 * @param string $password
	 * @param bool $checkPasswordStructure
	 * @throws kUserException::USER_NOT_FOUND
	 * @throws kUserException::USER_ALREADY_EXISTS
	 * @throws kUserException::INVALID_EMAIL
	 * @throws kUserException::INVALID_PARTNER
	 * @throws kUserException::ADMIN_LOGIN_USERS_QUOTA_EXCEEDED
	 * @throws kUserException::LOGIN_ID_ALREADY_USED
	 * @throws kUserException::PASSWORD_STRUCTURE_INVALID
	 * @throws kPermissionException::ROLE_ID_MISSING
	 * @throws kPermissionException::ONLY_ONE_ROLE_PER_USER_ALLOWED
	 */
	public static function addUser(kuser $user, $password = null, $checkPasswordStructure = true, $sendEmail = null)
	{
		if (!$user->getPuserId()) {
			throw new kUserException('', kUserException::USER_ID_MISSING);
		}
		
		// check if user with the same partner and puserId already exists		
		$existingUser = kuserPeer::getKuserByPartnerAndUid($user->getPartnerId(), $user->getPuserId());
		if ($existingUser) {
			throw new kUserException('', kUserException::USER_ALREADY_EXISTS);
		}
		
		// check if roles are valid - may throw exceptions
		if (!$user->getRoleIds() && $user->getIsAdmin()) {
			// assign default role according to user type admin / normal
			$userRoleId = $user->getPartner()->getAdminSessionRoleId();
			$user->setRoleIds($userRoleId);
		}
		UserRolePeer::testValidRolesForUser($user->getRoleIds(), $user->getPartnerId());
		
		if($user->getScreenName() === null) {
			$user->setScreenName($user->getPuserId());
		}
			
		if($user->getFullName() === null) {
			$user->setFirstName($user->getPuserId());
		}
		
		if (is_null($user->getStatus())) {
			$user->setStatus(KuserStatus::ACTIVE);
		}
		
		// if password is set, user should be able to login to the system - add a user_login_data record
		if ($password || $user->getIsAdmin()) {
			// throws an action on error
			$user->enableLogin($user->getEmail(), $password, $checkPasswordStructure, $sendEmail);
		}	
		
		$user->save();
		return $user;
	}
	
	
	
	public static function sendNewUserMailToAdmins(kuser $user)
	{
		$partnerId = $user->getPartnerId();
		$creatorUserName = 'Unknown';
		if (!is_null(kCurrentContext::$ks_uid))
		{
			$creatorUser = kuserPeer::getKuserByPartnerAndUid($partnerId, kCurrentContext::$ks_uid);
			if ($creatorUser) {
				$creatorUserName = $creatorUser->getFullName();
			}
		}
		$publisherName = PartnerPeer::retrieveByPK($partnerId)->getName();
		$loginEmail = $user->getEmail();
		$roleName = $user->getUserRoleNames();
		$puserId = $user->getPuserId();
		
		$bodyParams = null;


		$mailType = self::KALTURA_NEW_USER_EMAIL_TO_ADMINS;
		
		//If the new user partner is -2 (admin console) then it is a admin console user		
		if($partnerId == Partner::ADMIN_CONSOLE_PARTNER_ID)
		{
			$mailType = self::KALTURA_NEW_USER_ADMIN_CONSOLE_EMAIL_TO_ADMINS;
		}
				
		// get all partner administrators
		$c = new Criteria();
		$c->addAnd(kuserPeer::IS_ADMIN, true, Criteria::EQUAL);
		$c->addAnd(kuserPeer::PARTNER_ID, $partnerId, Criteria::EQUAL);
		$adminKusers = kuserPeer::doSelect($c);
		
		foreach ($adminKusers as $admin)
		{
			// don't send mail to the created user
			if ($admin->getId() == $user->getId())
			{
				continue;
			}
			
			// send email to all administrators with user management permissions
			if ($admin->hasPermissionOr(array(PermissionName::ADMIN_USER_ADD, PermissionName::ADMIN_USER_UPDATE, PermissionName::ADMIN_USER_DELETE)))
			{
				$adminName = $admin->getFullName();
				if (!$adminName) { $adminName = $admin->getPuserId(); }
				$unsubscribeLink .= $admin->getEmail();
				$bodyParams = null;
				
				if($partnerId == Partner::ADMIN_CONSOLE_PARTNER_ID) // Mail for admin console user
				{
					$bodyParams = array($adminName, $creatorUserName, $loginEmail, $roleName);
				}
				else
				{
					$bodyParams = array($adminName, $creatorUserName, $publisherName, $loginEmail, $publisherName, $roleName, $publisherName, $partnerId);
				}
				
				// add mail job
				kJobsManager::addMailJob(
					null, 
					0, 
					$partnerId, 
					$mailType, 
					kMailJobData::MAIL_PRIORITY_NORMAL, 
					kConf::get ("partner_registration_confirmation_email" ), 
					kConf::get ("partner_registration_confirmation_name" ), 
					$admin->getEmail(), 
					$bodyParams
				);
			}
		}
	}
	
	
	public static function sendNewUserMail(kuser $user, $existingUser)
	{
		// setup parameters
		$partnerId = $user->getPartnerId();
		$userName = $user->getFullName();
		if (!$userName) { $userName = $user->getPuserId(); }
		$creatorUserName = 'Unknown';
		if (!is_null(kCurrentContext::$ks_uid))
		{
			$creatorUser = kuserPeer::getKuserByPartnerAndUid($partnerId, kCurrentContext::$ks_uid);
			if ($creatorUser) {
				$creatorUserName = $creatorUser->getFullName();
			}
		}
		$publisherName = PartnerPeer::retrieveByPK($partnerId)->getName();
		$loginEmail = $user->getEmail();
		$roleName = $user->getUserRoleNames();
		$puserId = $user->getPuserId();
		if (!$existingUser) {
			$resetPasswordLink = UserLoginDataPeer::getPassResetLink($user->getLoginData()->getPasswordHashKey());
		}
		$kmcLink = trim(kConf::get('apphome_url'), '/').'/kmc';
		$adminConsoleLink = trim(kConf::get('admin_console_url'));
		$contactLink = kConf::get('contact_url');
		$beginnersGuideLink = kConf::get('beginners_tutorial_url');
		$quickStartGuideLink = kConf::get('quick_start_guide_url');
		
		// setup mail
		$mailType = null;
		$bodyParams = array();
		
		if($partnerId == Partner::ADMIN_CONSOLE_PARTNER_ID) // If new user is admin console user
		{
			if ($existingUser)
			{
				$mailType = self::KALTURA_NEW_EXISTING_USER_ADMIN_CONSOLE_EMAIL;
				$bodyParams = array($userName, $creatorUserName, $loginEmail, $roleName);
			}
			else
			{
				$mailType = self::KALTURA_NEW_USER_ADMIN_CONSOLE_EMAIL;
				$bodyParams = array($userName, $creatorUserName, $loginEmail, $resetPasswordLink, $roleName, $adminConsoleLink);
			}
		}
		else // Not an admin console partner
		{
			if ($existingUser)
			{
				$mailType = self::KALTURA_NEW_EXISTING_USER_EMAIL;
				$bodyParams = array($userName, $creatorUserName, $publisherName, $loginEmail, $partnerId, $publisherName, $publisherName, $roleName, $publisherName, $puserId, $kmcLink, $contactLink, $beginnersGuideLink, $quickStartGuideLink);
			}
			else
			{
				$mailType = self::KALTURA_NEW_USER_EMAIL;
				$bodyParams = array($userName, $creatorUserName, $publisherName, $loginEmail, $resetPasswordLink, $partnerId, $publisherName, $publisherName, $roleName, $publisherName, $puserId, $kmcLink, $contactLink, $beginnersGuideLink, $quickStartGuideLink);
			}		
		}
		// add mail job
		kJobsManager::addMailJob(
			null, 
			0, 
			$partnerId, 
			$mailType, 
			kMailJobData::MAIL_PRIORITY_NORMAL, 
			kConf::get ("partner_registration_confirmation_email" ), 
			kConf::get ("partner_registration_confirmation_name" ), 
			$loginEmail, 
			$bodyParams
		);
	}
			
	public static function getCacheInvalidationKeys()
	{
		return array(array("kuser:id=%s", self::ID), array("kuser:partnerId=%s,puserid=%s", self::PARTNER_ID, self::PUSER_ID));		
	}
	
	public static function retrieveByPKNoFilter($pk, PropelPDO $con = null)
	{
		self::setUseCriteriaFilter(false);
		$ret = self::retrieveByPK($pk, $con);
		self::setUseCriteriaFilter(true);
		return $ret;
	}
	
	/* (non-PHPdoc)
	 * @see IRelatedObjectPeer::getRootObjects()
	 */
	public function getRootObjects(IRelatedObject $object)
	{
		return array();
	}

	/* (non-PHPdoc)
	 * @see IRelatedObjectPeer::isReferenced()
	 */
	public function isReferenced(IRelatedObject $object)
	{
		return true;
	}
}
