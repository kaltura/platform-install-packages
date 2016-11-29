<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
				xmlns:ext="http://exslt.org/common"
				version="1.0">
<xsl:output omit-xml-declaration="no" method="xml" encoding="UTF-8" indent="no" />
<xsl:param name="BASE_DIR" />
<xsl:param name="APP_URL" />
<xsl:param name="ADMIN_SECRET" />
<xsl:param name="HOSTNAME" />
<xsl:template name="apply-copy">
	<xsl:param name="copy-element" select="." />
	<xsl:param name="indent"><xsl:text>
		</xsl:text></xsl:param>
	<xsl:choose>
		<xsl:when test="count($copy-element/*|$copy-element/comment())">
			<xsl:for-each select="$copy-element/*|$copy-element/comment()">
				<xsl:value-of select="$indent"/><xsl:text>	</xsl:text>
				<xsl:choose>
					<xsl:when test="self::comment()">
						<xsl:copy-of select="."/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:element name="{local-name(.)}">
							<xsl:call-template name="apply-copy">
								<xsl:with-param name="indent">
									<xsl:value-of select="$indent"/><xsl:text>	</xsl:text>
								</xsl:with-param>
							</xsl:call-template>
						</xsl:element>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:for-each>
			<xsl:value-of select="$indent"/>
		</xsl:when>
		<xsl:otherwise><xsl:value-of select="$copy-element"/></xsl:otherwise>
	</xsl:choose>
</xsl:template>
<xsl:template name="apply-property">
	<xsl:param name="property" select="." />
	<xsl:param name="indent" />
	
	<xsl:value-of select="$indent"/>
	<xsl:element name="Property">
		<xsl:call-template name="apply-copy">
			<xsl:with-param name="copy-element" select="$property" />
			<xsl:with-param name="indent" select="$indent" />
		</xsl:call-template>
	</xsl:element>
</xsl:template>
<xsl:template name="apply-properties">
	<xsl:param name="set-properties" />
	<xsl:param name="existing-properties" select="." />
	<xsl:param name="indent"><xsl:text>
			</xsl:text></xsl:param>
	<xsl:param name="indent-plus"><xsl:value-of select="$indent" /><xsl:text>	</xsl:text></xsl:param>
	
	<xsl:for-each select="*">
		<xsl:variable name="existing-property-name" select="string(Name)" />
		<xsl:choose>
			<xsl:when test="count(ext:node-set($set-properties)/Property[Name = $existing-property-name]) > 0">
				<xsl:call-template name="apply-property">
					<xsl:with-param name="property" select="ext:node-set($set-properties)/Property[Name = $existing-property-name]"/>
					<xsl:with-param name="indent" select="$indent-plus" />
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="apply-property">
					<xsl:with-param name="indent" select="$indent-plus" />
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
	
	<xsl:for-each select="ext:node-set($set-properties)/*">
		<xsl:variable name="set-property-name" select="string(Name)" />
		<xsl:if test="count($existing-properties/Property[Name = $set-property-name]) = 0">
			<xsl:call-template name="apply-property">
				<xsl:with-param name="indent" select="$indent-plus" />
			</xsl:call-template>
		</xsl:if>
	</xsl:for-each>
	<xsl:value-of select="$indent" />
</xsl:template>
<xsl:template name="application-streams">
	<xsl:for-each select="*|comment()">
			<xsl:text>
			</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'StreamType'">live</xsl:when>
						<xsl:when test="local-name(.) = 'StorageDir'">
							<xsl:value-of select="$BASE_DIR" />
							<xsl:text>/web/content/recorded/</xsl:text>
                            <xsl:value-of select="$HOSTNAME" />
						</xsl:when>
						<xsl:when test="local-name(.) = 'LiveStreamPacketizers'">cupertinostreamingpacketizer, dvrstreamingpacketizer, mpegdashstreamingpacketizer, sanjosestreamingpacketizer, smoothstreamingpacketizer</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
		<xsl:text>
		</xsl:text>
</xsl:template>
<xsl:template name="application-transcoder">
	<xsl:for-each select="*|comment()">
			<xsl:text>
			</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'LiveStreamTranscoder'">transcoder</xsl:when>
						<xsl:when test="local-name(.) = 'Templates'">
							<xsl:value-of select="$APP_URL" />
							<xsl:text>/api_v3/index.php/service/wowza_liveConversionProfile/action/serve/streamName/${SourceStreamName}/f/transcode.xml</xsl:text>
						</xsl:when>
						<xsl:when test="local-name(.) = 'Properties'">
							<xsl:call-template name="apply-properties">
								<xsl:with-param name="set-properties">
									<Property>
										<Name>sortPackets</Name>
										<Value>true</Value>
										<Type>Boolean</Type>
									</Property>
									<Property>
										<Name>sortBufferSize</Name>
										<Value>4000</Value>
										<Type>Integer</Type>
									</Property>
								</xsl:with-param>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
		<xsl:text>
		</xsl:text>
</xsl:template>
<xsl:template name="application-dvr">
	<xsl:for-each select="*|comment()">
			<xsl:text>
			</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'Recorders'">dvrrecorder</xsl:when>
						<xsl:when test="local-name(.) = 'Store'">dvrfilestorage</xsl:when>
						<xsl:when test="local-name(.) = 'WindowDuration'">14400</xsl:when>
						<xsl:when test="local-name(.) = 'StorageDir'">
							<xsl:value-of select="$BASE_DIR" />
							<xsl:text>var/live/dvr</xsl:text>
						</xsl:when>
						<xsl:when test="local-name(.) = 'Properties'">
							<xsl:call-template name="apply-properties">
								<xsl:with-param name="set-properties">
									<Property>
										<Name>httpRandomizeMediaName</Name>
										<Value>true</Value>
										<Type>boolean</Type>
									</Property>
									<Property>
										<Name>calculateChunkIDBasedOnTimecode</Name>
										<Value>true</Value>
										<Type>boolean</Type>
									</Property>
									<Property>
										<Name>dvrAudioOnlyChunkTargetDuration</Name>
										<Value>10000</Value>
										<Type>Integer</Type>
									</Property>
									<Property>
										<Name>dvrChunkDurationMinimum</Name>
										<Value>10000</Value>
										<Type>Integer</Type>
									</Property>
									<Property>
										<Name>dvrMinimumAvailableChunks</Name>
										<Value>3</Value>
										<Type>Integer</Type>
									</Property>
								</xsl:with-param>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
		<xsl:text>
		</xsl:text>
</xsl:template>
<xsl:template name="application-rtp-authentication">
	<xsl:for-each select="*|comment()">
				<xsl:text>
				</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'PublishMethod'">none</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
		<xsl:text>
			</xsl:text>
</xsl:template>
<xsl:template name="application-rtp">
	<xsl:for-each select="*|comment()">
			<xsl:text>
			</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'Authentication'"><xsl:call-template name="application-rtp-authentication"/></xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
		<xsl:text>
		</xsl:text>
</xsl:template>
<xsl:template name="application-live_stream_packetizer">
	<xsl:for-each select="*|comment()">
			<xsl:text>
			</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'Properties'">
							<xsl:call-template name="apply-properties">
								<xsl:with-param name="set-properties">
									<Property>
										<Name>httpRandomizeMediaName</Name>
										<Value>true</Value>
										<Type>boolean</Type>
									</Property>
									<Property>
										<Name>calculateChunkIDBasedOnTimecode</Name>
										<Value>true</Value>
										<Type>boolean</Type>
									</Property>
									<Property>
										<Name>cupertinoCalculateChunkIDBasedOnTimecode</Name>
										<Value>true</Value>
										<Type>boolean</Type>
									</Property>
									<Property>
										<Name>cupertinoChunkDurationTarget</Name>
										<Value>10000</Value>
										<Type>Integer</Type>
									</Property>
									<Property>
										<Name>cupertinoMaxChunkCount</Name>
										<Value>20</Value>
										<Type>Integer</Type>
									</Property>
									<Property>
										<Name>cupertinoPlaylistChunkCount</Name>
										<Value>10</Value>
										<Type>Integer</Type>
									</Property>
									<Property>
										<Name>sanjoseChunkDurationTarget</Name>
										<Value>10000</Value>
										<Type>Integer</Type>
									</Property>
									<Property>
										<Name>sanjoseMaxChunkCount</Name>
										<Value>20</Value>
										<Type>Integer</Type>
									</Property>
									<Property>
										<Name>sanjosePlaylistChunkCount</Name>
										<Value>10</Value>
										<Type>Integer</Type>
									</Property>
									<Property>
										<Name>cupertinoPacketizeAllStreamsAsTS</Name>
										<Value>true</Value>
										<Type>Boolean</Type>
									</Property>
								</xsl:with-param>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
		<xsl:text>
		</xsl:text>
</xsl:template>

<xsl:template name="application-client">
	<xsl:for-each select="*|comment()">
	<xsl:text>
	</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'Access'">
							<xsl:call-template name="application-client-access"></xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
<xsl:text>
</xsl:text>
</xsl:template>


<xsl:template name="application-client-access">
	<xsl:for-each select="*|comment()">
	<xsl:text>
	</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'StreamWriteAccess'">
							<xsl:text>*</xsl:text>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy">
								<!--<xsl:with-param name="indent"  />-->
							</xsl:call-template>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
<xsl:text>
</xsl:text>
</xsl:template>
<xsl:template name="application-http_streamer">
	<xsl:for-each select="*|comment()">
			<xsl:text>
			</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'Properties'">
							<xsl:call-template name="apply-properties">
								<xsl:with-param name="set-properties">
									<Property>
										<Name>httpOriginMode</Name>
										<Value>on</Value>
									</Property>
									<Property>
										<Name>calculateChunkIDBasedOnTimecode</Name>
										<Value>true</Value>
										<Type>boolean</Type>
									</Property>
									<Property>
										<Name>cupertinoCalculateChunkIDBasedOnTimecode</Name>
										<Value>true</Value>
										<Type>boolean</Type>
									</Property>
									<Property>
										<Name>cupertinoCacheControlPlaylist</Name>
										<Value>max-age=5</Value>
									</Property>
									<Property>
										<Name>cupertinoCacheControlMediaChunk</Name>
										<Value>max-age=86400</Value>
									</Property>
									<Property>
										<Name>cupertinoOnChunkStartResetCounter</Name>
										<Value>false</Value>
										<Type>boolean</Type>
									</Property>
									<Property>
										<Name>cupertinoCalculateCodecs</Name>
										<Value>false</Value>
										<Type>Boolean</Type>
									</Property>
									<Property>
										<Name>smoothCacheControlPlaylist</Name>
										<Value>max-age=3</Value>
									</Property>
									<Property>
										<Name>smoothCacheControlMediaChunk</Name>
										<Value>max-age=86400</Value>
									</Property>
									<Property>
										<Name>smoothCacheControlDataChunk</Name>
										<Value>max-age=86400</Value>
									</Property>
									<Property>
										<Name>sanjoseCacheControlPlaylist</Name>
										<Value>max-age=3</Value>
									</Property>
									<Property>
										<Name>sanjoseCacheControlMediaChunk</Name>
										<Value>max-age=86400</Value>
									</Property>
									<Property>
										<Name>cupertinoUserHTTPHeaders</Name>
										<Value>Access-Control-Allow-Origin: *</Value>
									</Property>
								</xsl:with-param>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
		<xsl:text>
		</xsl:text>
</xsl:template>
<xsl:template name="application-manager">
	<xsl:for-each select="*|comment()">
			<xsl:text>
			</xsl:text>
		<xsl:choose>
			<xsl:when test="self::comment()">
				<xsl:copy-of select="."/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{local-name(.)}">
					<xsl:choose>
						<xsl:when test="local-name(.) = 'Properties'">
							<xsl:call-template name="apply-properties">
								<xsl:with-param name="set-properties">
									<Property>
										<Name>DVREnable</Name>
										<Value>true</Value>
										<Type>Boolean</Type>
									</Property>
								</xsl:with-param>
							</xsl:call-template>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="apply-copy" />
						</xsl:otherwise>
					</xsl:choose>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
		<xsl:text>
		</xsl:text>
</xsl:template>
<xsl:template name="application-modules">
	<xsl:for-each select="*">
			<xsl:text>
			</xsl:text>
		<xsl:element name="{local-name(.)}">
			<xsl:choose>
				<xsl:when test="string(Name) != 'LiveStreamEntry'">
					<xsl:call-template name="apply-copy">
						<xsl:with-param name="indent">
			<xsl:text>
			</xsl:text>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
			</xsl:choose>
		</xsl:element>
	</xsl:for-each>
	<xsl:variable name="live-stream-entry-module">
		<Module>
			<Name>ModuleCoreSecurity</Name>
			<Description>Core Security Module for Applications</Description>
			<Class>com.wowza.wms.security.ModuleCoreSecurity</Class>
		</Module>
		<Module>
			<Name>LiveStreamEntry</Name>
			<Description>LiveStreamEntry</Description>
			<Class>com.kaltura.media.server.wowza.listeners.LiveStreamEntry</Class>
		</Module>
		<Module>
			<Name>ModuleRTMPPublishDebug</Name>
			<Description>WowzaDebugModule</Description>
			<Class>com.kaltura.media.server.wowza.ModuleRTMPPublishDebug</Class>
		</Module>
		<Module>
			<Name>CuePointManager</Name>
			<Description>CuePointManager</Description>
			<Class>com.kaltura.media.server.wowza.CuePointsManager</Class>
		</Module>
	</xsl:variable>
	<xsl:call-template name="apply-copy">
		<xsl:with-param name="copy-element" select="ext:node-set($live-stream-entry-module)" />
	</xsl:call-template>
</xsl:template>

<xsl:template name="application">
	<xsl:text>
	</xsl:text>
	<xsl:element name="Application">
		<xsl:for-each select="*|comment()">
		<xsl:text>
		</xsl:text>
			<xsl:choose>
				<xsl:when test="self::comment()">
					<xsl:copy-of select="."/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="{local-name(.)}">
						<xsl:choose>
							<xsl:when test="local-name(.) = 'Name'">kLive</xsl:when>
							<xsl:when test="local-name(.) = 'AppType'">Live</xsl:when>
							<xsl:when test="local-name(.) = 'Streams'"><xsl:call-template name="application-streams"/></xsl:when>
							<xsl:when test="local-name(.) = 'Transcoder'"><xsl:call-template name="application-transcoder"/></xsl:when>
							<xsl:when test="local-name(.) = 'DVR'"><xsl:call-template name="application-dvr"/></xsl:when>
							<xsl:when test="local-name(.) = 'HTTPStreamers'">cupertinostreaming, smoothstreaming, sanjosestreaming, mpegdashstreaming, dvrchunkstreaming</xsl:when>
							<xsl:when test="local-name(.) = 'RTP'"><xsl:call-template name="application-rtp"/></xsl:when>
							<xsl:when test="local-name(.) = 'LiveStreamPacketizer'"><xsl:call-template name="application-live_stream_packetizer"/></xsl:when>
							<xsl:when test="local-name(.) = 'HTTPStreamer'"><xsl:call-template name="application-http_streamer"/></xsl:when>
							<xsl:when test="local-name(.) = 'Manager'"><xsl:call-template name="application-manager"/></xsl:when>
							<xsl:when test="local-name(.) = 'Modules'"><xsl:call-template name="application-modules"/></xsl:when>
							<xsl:when test="local-name(.) = 'Client'"><xsl:call-template name="application-client"/></xsl:when>
							<xsl:when test="local-name(.) = 'Properties'">
								<xsl:call-template name="apply-properties">
									<xsl:with-param name="indent"><xsl:text>
		</xsl:text></xsl:with-param>
									<xsl:with-param name="set-properties">
										<Property>
											<Name>securityPublishRequirePassword</Name>
											<Value>false</Value>
											<Type>Boolean</Type>
										</Property>
										<Property>
											<Name>securityPublishBlockDuplicateStreamNames</Name>
											<Value>true</Value>
											<Type>Boolean</Type>
										</Property>
										<Property>
											<Name>streamTimeout</Name>
											<Value>200</Value>
											<Type>Integer</Type>
										</Property>
										<!--<Property>-->
											<!--<Name>ApplicationManagers</Name>-->
											<!--<Value>com.kaltura.media.server.wowza.CuePointsManager</Value>-->
											<!--<Type>String</Type>-->
										<!--</Property>-->
										<Property>
											<Name>KalturaSyncPointsInterval</Name>
											<Value>4000</Value>
											<Type>Integer</Type>
										</Property>
										<Property>
											<Name>readyForPlaybackMinimumChunkCount</Name>
											<Value>4</Value>
											<Type>Integer</Type>
										</Property>
									</xsl:with-param>
								</xsl:call-template>
							</xsl:when>
							<xsl:otherwise>
								<xsl:call-template name="apply-copy">
									<xsl:with-param name="indent">
		<xsl:text>
		</xsl:text>
									</xsl:with-param>
								</xsl:call-template>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	<xsl:text>
	</xsl:text>
	</xsl:element>
	<xsl:text>
</xsl:text>
</xsl:template>
<xsl:template match="/Root/Application">
	<xsl:element name="Root">
		<xsl:attribute name="version">1</xsl:attribute>
		<xsl:call-template name="application"/>
	</xsl:element>
</xsl:template>

<xsl:template name="server-listeners">
	<xsl:for-each select="*">
			<xsl:text>
			</xsl:text>
		<xsl:element name="{local-name(.)}">
			<xsl:choose>
				<xsl:when test="string(BaseClass) != 'com.kaltura.media.server.wowza.listeners.ServerListener'">
					<xsl:call-template name="apply-copy">
						<xsl:with-param name="indent">
			<xsl:text>
			</xsl:text>
						</xsl:with-param>
					</xsl:call-template>
				</xsl:when>
			</xsl:choose>
		</xsl:element>
	</xsl:for-each>
	<xsl:variable name="kaltura-server-listener">
		<ServerListener>
			<BaseClass>com.kaltura.media.server.wowza.listeners.ServerListener</BaseClass>
		</ServerListener>
	</xsl:variable>
	<xsl:call-template name="apply-copy">
		<xsl:with-param name="copy-element" select="ext:node-set($kaltura-server-listener)" />
	</xsl:call-template>
</xsl:template>

<xsl:template name="server">
	<xsl:text>
	</xsl:text>
	<xsl:element name="Server">
		<xsl:for-each select="*|comment()">
		<xsl:text>
		</xsl:text>
			<xsl:choose>
				<xsl:when test="self::comment()">
					<xsl:copy-of select="."/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:element name="{local-name(.)}">
						<xsl:choose>
							<xsl:when test="local-name(.) = 'ServerListeners'"><xsl:call-template name="server-listeners"/></xsl:when>
							<xsl:when test="local-name(.) = 'Properties'">
								<xsl:call-template name="apply-properties">
									<xsl:with-param name="indent"><xsl:text>
		</xsl:text></xsl:with-param>
									<xsl:with-param name="set-properties">
										<Property>
											<Name>KalturaServerURL</Name>
											<Value><xsl:value-of select="$APP_URL" /></Value>
										</Property>
										<Property>
											<Name>KalturaServerAdminSecret</Name>
											<Value><xsl:value-of select="$ADMIN_SECRET" /></Value>
										</Property>
										<Property>
											<Name>KalturaServerTimeout</Name>
											<Value>180</Value>
										</Property>
										<Property>
											<Name>KalturaServerManagers</Name>
											<!--list of managers to be loaded-->
											<Value>com.kaltura.media.server.wowza.LiveStreamManager, com.kaltura.media.server.wowza.PushPublishManager</Value>
										</Property>
										<Property>
											<Name>KalturaServerWebServices</Name>
											<Value>com.kaltura.media.server.api.services.KalturaLiveService</Value>
										</Property>
										<Property>
											<Name>KalturaServerStatusInterval</Name>
											<!-- the interval in seconds to send the status to the API -->
											<Value>300</Value>
										</Property>
										<Property>
											<Name>KalturaLiveStreamKeepAliveInterval</Name>
											<!-- the interval in seconds to update that live stream entry is still broadcasting -->
											<Value>30</Value>
										</Property>
										<Property>
											<Name>KalturaLiveStreamMaxDvrWindow</Name>
											<Value>86400</Value>
										</Property>
										<Property>
											<Name>KalturaChannelLockStartTimeOffset</Name>
											<Value/>
										</Property>
										<Property>
											<Name>KalturaMaxChannelsLocks</Name>
											<Value/>
										</Property>
										<Property>
											<Name>KalturaRecordedChunckMaxDuration</Name>
											<Value>60</Value>
										</Property>
										<Property>
											<Name>KalturaServerWebServicesPort</Name>
											<Value>888</Value>
										</Property>
										<Property>
											<Name>KalturaServerWebServicesHost</Name>
											<Value>0.0.0.0</Value>
										</Property>
										<Property>
											<Name>KalturaRecordedFileGroup</Name>
											<Value>kaltura</Value>
										</Property>
										<Property>
											<Name>KalturaIsLiveRegistrationMinBufferTime</Name>
											<Value>30</Value>
										</Property>
									</xsl:with-param>
								</xsl:call-template>
							</xsl:when>
							<xsl:otherwise>
								<xsl:call-template name="apply-copy">
									<xsl:with-param name="indent">
		<xsl:text>
		</xsl:text>
									</xsl:with-param>
								</xsl:call-template>
							</xsl:otherwise>
						</xsl:choose>
					</xsl:element>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	<xsl:text>
	</xsl:text>
	</xsl:element>
	<xsl:text>
</xsl:text>
</xsl:template>

<xsl:template match="/Root/Server">
	<xsl:element name="Root">
		<xsl:attribute name="version">2</xsl:attribute>
		<xsl:call-template name="server"/>
	</xsl:element>
</xsl:template>

</xsl:stylesheet>
