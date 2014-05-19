NAME = 'LIVE with Kelly and Michael'
ICON = 'icon-default.jpg'
ART = 'art-default.jpg'

FEED = 'http://c.brightcove.com/services/json/experience/runtime/?command=get_programming_for_experience&playerKey=AQ~~,AAAAABGr2I4~,jeitpkmmkDnPxnGRjOqBdXFyftAKAtKg'

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'

####################################################################################################
@handler('/video/livewithkellyandmichael', NAME, thumb=ICON, art=ART, allow_sync=True)
def MainMenu():

	oc = ObjectContainer()

	for item in JSON.ObjectFromURL(FEED)['videoList']['mediaCollectionDTO']['videoDTOs']:

		url = None

		for video in item['renditions']:
			if video['frameHeight'] == 576:
				url = video['defaultURL']
				break

		if not url:
			url = item['FLVFullLengthURL']

		title = item['displayName']
		summary = item['shortDescription']
		thumb = item['videoStillURL']
		originally_available_at = Datetime.FromTimestamp(int(item['publishedDate'])/1000)

		oc.add(CreateVideoClipObject(
			url = url,
			title = title,
			summary = summary,
			thumb = thumb,
			originally_available_at = originally_available_at
		))

	return oc

####################################################################################################
def CreateVideoClipObject(url, title, summary, thumb, originally_available_at, include_container=False):

	videoclip_obj = VideoClipObject(
		key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary, thumb=thumb, originally_available_at=originally_available_at, include_container=True),
		rating_key = url,
		title = title,
		summary = summary,
		thumb = Resource.ContentsOfURLWithFallback(url=thumb, fallback=ICON),
		originally_available_at = originally_available_at,
		art = R(ART),
		items = [
			MediaObject(
				parts = [
					PartObject(key=url)
				],
				container = Container.MP4,
				video_codec = VideoCodec.H264,
				video_resolution = '576',
				audio_codec = AudioCodec.AAC,
				audio_channels = 2,
				optimized_for_streaming = True
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[videoclip_obj])
	else:
		return videoclip_obj
