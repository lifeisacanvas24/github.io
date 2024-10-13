## Hi there 👋

<!--
**lifeisacanvas24/lifeisacanvas24** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Pagination
IG / YT datafeed
To integrate an Instagram feed into your Zola-based site, you’ll need to follow these steps:

1. Use an Instagram API or Third-Party Service

There are two main approaches to adding an Instagram feed to your site:

	1.	Instagram’s Graph API (official but requires creating an app, managing access tokens, etc.)
	2.	Third-Party Services (simpler but may come with limitations or branding)

Option 1: Using Instagram’s Graph API

To use the Instagram API:

	1.	Create a Facebook App:
	•	Go to the Facebook for Developers website and create an app.
	•	Get access to Instagram Basic Display or Instagram Graph API.
	2.	Get Access Tokens:
	•	Follow the Instagram Graph API Guide to get an access token.
	3.	Fetch Instagram Feed:
Use curl or a HTTP library (e.g., using JavaScript’s fetch API) to request recent posts via Instagram’s API. For example:
curl -X GET "https://graph.instagram.com/me/media?fields=id,caption,media_url&access_token=YOUR_ACCESS_TOKEN"

	Display the Feed in Zola:
Write a custom shortcode or macro in Zola that fetches the feed and displays it in your templates.

Example JavaScript Code for Fetching Instagram Feed:
<script>
  fetch('https://graph.instagram.com/me/media?fields=id,media_url,caption&access_token=YOUR_ACCESS_TOKEN')
    .then(response => response.json())
    .then(data => {
      let output = '';
      data.data.forEach(post => {
        output += `<div class="instagram-post">
                     <img src="${post.media_url}" alt="Instagram Image">
                     <p>${post.caption}</p>
                   </div>`;
      });
      document.getElementById('instagram-feed').innerHTML = output;
    })
    .catch(err => console.log(err));
</script>

In your Zola template (index.html or any other page), you would have something like this to display the feed:
<div id="instagram-feed"></div>

Option 2: Using a Third-Party Service

If you prefer a simpler approach, you can use third-party services that allow you to embed Instagram feeds:

	1.	Embed Instagram Feed Using Tools like SnapWidget or LightWidget
	•	Services like SnapWidget or LightWidget allow you to create Instagram widgets with minimal effort.
	•	Sign up for one of these services and customize the widget (size, layout, etc.).
	•	After customization, you’ll get an embed code that you can place in your Zola template.

<div class="instagram-feed">
  <iframe src="https://snapwidget.com/embed/xxxx" allowtransparency="true" frameborder="0" scrolling="no" style="border:none; overflow:hidden; width:100%; height:400px"></iframe>
</div>

2. Add Instagram Feed to Your Zola Template

After choosing an approach, add the appropriate code to your Zola layout or page templates.

Example Template Usage:

If you’re using a third-party widget, add the widget code to your Zola template. For example, in your base.html or index.html:

<section class="section">
  <div class="container">
    <h2 class="title is-4">Our Instagram Feed</h2>
    <!-- Add Instagram Feed Embed Code -->
    <div class="instagram-feed">
      <iframe src="https://snapwidget.com/embed/xxxx" allowtransparency="true" frameborder="0" scrolling="no" style="border:none; overflow:hidden; width:100%; height:400px"></iframe>
    </div>
  </div>
</section>

Styling with Bulma:

You can apply Bulma classes to style the feed nicely.
<section class="section">
  <div class="container">
    <h2 class="title is-4">Follow us on Instagram</h2>
    <div class="columns is-multiline">
      <div class="column is-one-quarter">
        <!-- Instagram post goes here -->
      </div>
      <!-- Repeat for other posts -->
    </div>
  </div>
</section>


content for the entire website
dynamic parts to be handle using astro.build
defining .md template
exploring more commoponents from bulma
daisy css
