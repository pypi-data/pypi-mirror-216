require([
  'jquery',
  'node_modules/@microsoft/immersive-reader-sdk/lib/immersive-reader-sdk',
], function($, ImmersiveReader) {
  'use strict';

  $(document).ready(function() {
    // immersive reader
    function getTokenAndSubdomainAsync() {
      return new Promise(function(resolve, reject) {
        $.ajax({
          url: $('body').data('portalUrl') + '/@immersive-reader-token',
          type: 'GET',
          headers: { Accept: 'application/json' },
          success: function(data) {
            if (data.error) {
              reject(data.error);
            } else {
              resolve(data);
            }
          },
          error: function(err) {
            reject(err);
          },
        });
      });
    }

    function handleLaunchImmersiveReader() {
      getTokenAndSubdomainAsync()
        .then(function(response) {
          var token = response.token;
          var subdomain = response.subdomain;
          var content = '';
          if ($('body').hasClass('template-rernews_view')) {
            content = $('.news-text').html() || '';
          } else if ($('body').hasClass('portaltype-bando')) {
            content = $('.rer-contextual-text').html() || '';
          } else if ($('body').hasClass('portaltype-event')) {
            var details = $('.event.summary.details').html() || '';
            var text = $('#parent-fieldname-text').html() || '';
            content = details + text;
          } else if (
            $('body').hasClass('template-collection_bandi_view') ||
            $('body').hasClass('template-collection_bandi_tipologia_view')
          ) {
            content = $('#content .document-text').html() || '';
          } else {
            content = $('#content-core').html() || '';
          }

          // Learn more about chunk usage and supported MIME types https://docs.microsoft.com/azure/cognitive-services/immersive-reader/reference#chunk
          var data = {
            title: $('h1.documentFirstHeading').text(),
            chunks: [
              {
                content: content,
                mimeType: 'text/html',
              },
            ],
          };

          // Learn more about options https://docs.microsoft.com/azure/cognitive-services/immersive-reader/reference#options
          var options = {
            // onExit: exitCallback,
            uiZIndex: 2000,
          };

          ImmersiveReader.launchAsync(token, subdomain, data, options).catch(
            function(error) {
              alert('Impossibile caricare Immersive Reader.');
              console.error(error);
            }
          );
        })
        .catch(function(error) {
          alert('Impossibile caricare Immersive Reader.');
          console.error(error);
        });
    }

    $('.template-rernews_view #immersive-reader-wrapper').insertBefore(
      '.template-rernews_view .news-text'
    );

    $('.immersive-reader-link').click(function() {
      handleLaunchImmersiveReader();
    });

    function exitCallback() {
      alert('Impossibile caricare Immersive Reader.');
    }
  });
});
