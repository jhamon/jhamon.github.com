---
layout: post
title: "Keeping your secrets safe with figaro"
date: 2014-1-08 22:22:01 -0700
comments: true
categories: rails
---

While working on several of my side projects, I've often had a need to store secret information in my project.  I need a way to make things like API keys available to my application without accidentally exposing them to others when, for instance, I push that code to Github or Bitbucket. 

Many people much smarter than myself have thought about the problem of managing secrets, and one the suggested solutions is to [store configuration information in the environment](http://12factor.net/config). The advantage of this approach, besides keeping your credentials out of your git history, is that it allows you to easily configure environment-specific as needed by keeping the things that change (the API keys) seperate from the application being deployed.  

An example of how this might come into play would be if your application was integrated with a third-party API, like a payment processor, operating on stateful resources.  You probably want to use different API keys for each environment to avoid accidentally charging your customers from dev or staging. Because even if you are writing a lot of tests, you never know for sure that something horrible and unexpected won't happen when you first roll out a new feature. 

Keeping environment-specific configuration seperate from the application makes avoiding a horror scenario relatively easy.

## Configuration with Figaro

Fortunately for us, other people have done the necessary legwork to implement this.  In Rails 4.1, we should be using [`secrets.yml`](http://guides.rubyonrails.org/4_1_release_notes.html#config-secrets-yml) to hold confidential information.  But for those still on Rails 3, there's a nice gem called [`figaro`](https://github.com/laserlemon/figaro) that does the work of populating environment variables from a configuration file (not checked into version control) for us.

First add the gem to your gemfile

```ruby
  # Gemfile
  gem 'figaro'
```

And install it from the command line

```ruby
  bundle install && figaro install
```

The `figaro install` command creates a `config/application.yml` file and adds it to `.gitignore` so that it cannot be checked into version control.

Now we're ready to add some configuration.

```yaml
# config/application.yml

staging:
  twilio_account_sid: "not_a_real_account_sid_but_you_get_the_idea"
  twilio_auth_token: "auth_auth_auth_auth_auth_auth_"

production:
  twilio_account_sid: "a_totally_different_fake_account_sid"
  twilio_auth_token: "a_fake_auth_token"
```

When our rails application starts, figaro will make the appropriate credentials available in the `ENV` variable.  We can access these anyway, but often we'll do it in an initializer like this:

```ruby
# config/initializers/twilio.rb
Twilio.configure do |config|
  config.account_sid = ENV['twilio_account_sid']  
  config.auth_token  = ENV['twilio_auth_token']
end
```

### Don't get tripped up
One gotcha to keep in mind is that `ENV` is just a simple key value store holding strings. If you try to configure a variable to `false`, you'll run into trouble because `ENV['something_false']` will actually be the string `"false"`, which is truthy. Be vigilant.

## Secure your application secret token, too

If you're publishing your application source code publically while also deploying it, you may have inadvertantly exposed your application's secret token. The token is used to sign cookies, so you have [opened yourself up to being hacked](http://robertheaton.com/2013/07/22/how-to-hack-a-rails-app-using-its-secret-token/) if you publish a git repo with this information anywhere in its history. 

If you need to, generate a new secret token with `rake secret`. Then store that secret in your `config/application.yml` and update `config/initializers/secret_token.rb` accordingly.

```yaml
# config/application.yml
secret_token_base: '63683ebbd2fe8a4cb670c727e84b6cc2b5efb5814374dd9299490217b84c4ca4e826094c1fcb34df3d66c902b659acfae1e79d0e912a0828c53f1be72fe6f5e0'
```

```ruby
# config/initializers/secret_token.rb
MyApp::Application.config.secret_key_base = ENV['secret_token_base']
```




