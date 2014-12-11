oauth1-forpy3
=============
Makes using oAuth v1 simple

Simple instructions:
  1. Create an instance of the Client object. You must have:
      * a consumer key and secret, received from the site you're accessing
      * a user agent
  2. If you already have an access key and secret:
      * Client.set_access_token(your key,your secret)
     Else 
      * call Client.set_access_token() and it will use the consumer key and secret to acquire them
      * (if you want to then get the access token and secret for further use, call .access_token and .access_token_secret)
  3. Use Client.retrieve_page(url) and it will return it as a utf-8 encoded string
