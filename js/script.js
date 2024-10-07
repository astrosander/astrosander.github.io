(window, document, "script", "https://www.googletagmanager.com/gtag/js?id=G-9L31WBESWQ", "ym");
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'G-9L31WBESWQ');

// Function to add Google Tag Manager to the head
function addGoogleTagManagerToHead() {
    var gtmScript = document.createElement('script');
    gtmScript.innerHTML = `(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-KC6SSTZW');`;
    document.head.appendChild(gtmScript);
}

// Function to add Google Tag Manager noscript to the body
function addGoogleTagManagerNoscriptToBody() {
    var gtmNoscript = document.createElement('noscript');
    gtmNoscript.innerHTML = `<iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KC6SSTZW"
    height="0" width="0" style="display:none;visibility:hidden"></iframe>`;
    document.body.insertBefore(gtmNoscript, document.body.firstChild);
}

// Execute functions to add GTM code
addGoogleTagManagerToHead();
addGoogleTagManagerNoscriptToBody();