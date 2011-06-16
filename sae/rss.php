<?php
include_once('config.php');
include_once('saet.ex.class.php');

function clickable($text) {
	$html = preg_replace(
		'/(?<!S)((http(s?):\/\/)|(www.))+([\w.1-9\&=#?\-~%;\/]+)/',
		'<a href="http$3://$4$5">http$3://$4$5</a>', $text);
	return ($html);
}


$c = new SaeTClient(WB_AKEY, WB_SKEY, OAUTH_TOKEN, OAUTH_TOKEN_SECRET);
$user = $_REQUEST["id"];
if (empty($user)) {
	header('Content-Type:text/plain; charset=utf-8');
	echo "404 not found";
	exit(0);
}

$tl = $c->user_timeline(1, 200, $user);

if (is_array($tl) && count($tl) > 0) {
	header('Content-Type:text/xml; charset=utf-8');
	$domain = $tl[0]["user"]["domain"];
	if (empty($domain)) {
		$domain = $tl[0]["user"]["id"];
	}

	printf("<?xml version=\"1.0\" encoding=\"utf-8\" ?>
<rss version=\"2.0\">
  <channel>
  <title>
    weibo.com/%s
  </title>
  <link>
    http://weibo.com/%s
  </link>
  <description>
    %s的微博
  </description>
  <lastBuildDate>
    %s
  </lastBuildDate>
  <ttl>
    30
  </ttl>", $tl[0]["user"]["name"], $domain, $tl[0]["user"]["name"], gmdate(DATE_RFC822));

	foreach ($tl as $item) {
		$text = $item["text"];
		if (array_key_exists("retweeted_status", $item)) {
		    $text .= " || @" . $item["retweeted_status"]["user"]["name"] . ": " .  $item["retweeted_status"]["text"];
  		    if (array_key_exists("original_pic", $item["retweeted_status"])) {
				$text .= " " . $item["retweeted_status"]["original_pic"];
			}
		}

		if (array_key_exists("original_pic", $item)) {
		    $text .= " " . $item["original_pic"];
		}

		$title = $text;

		$link = "http://api.t.sina.com.cn/" . $item["user"]["id"] . "/statuses/" . $item["id"];
		$pubDate = $item["created_at"];
		printf("<item>
		  <title><![CDATA[%s]]></title>
		  <description><![CDATA[%s]]></description>
		  <link>%s</link>
		  <pubDate><![CDATA[%s]]></pubDate>
		  <guid isPermaLink=\"true\">%s</guid></item>", $title, clickable($text), $link, $pubDate, $link);
	}
	echo "</channel>
</rss>	 ";
} else {
	header('Content-Type:text/plain; charset=utf-8');
	echo "404 not found";
}

?>