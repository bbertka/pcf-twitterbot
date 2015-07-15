PCF-TwitterBot
=========

## A Pivotal Cloud Foundry Twitterbot and D3 Bubble Chart Visualization

[![Screenshot](https://raw.githubusercontent.com/bbertka/pcf-twitterbot/master/static/img/screenshot.png)](#)


To run, first vendor dependencies as found in requirements.txt:

<pre>
mkdir vendor
pip install --download vendor -r requirements.txt
</pre>

Update manifest.yml with your chosen app name (default is pybot), twitter app keys, and hashes to search -- then push!

<pre>
cf push
</pre>

If you want to add or remove hashtags, just update the environment variables in web console and restage:

<pre>
cf restage
</pre>


View the D3 bubble chart at your apps URL within a javascript friendly browser
