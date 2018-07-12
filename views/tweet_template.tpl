It looks like no coordinates were supplied with these tweets
<ul>
  % for tweet in tweet_details:
    <li>{{tweet['tweeter']}} says {{tweet['tweet']}}</li>
  % end
</ul>