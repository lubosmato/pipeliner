# Pipeliner
Pipeliner can do several anoying repetitive tasks for you. For example imagine you want to get an email when a certain blog publishes a new article. Or you are loving husband/wife and you want send some nice messages to your wife/husband repetitively. Or imagine you must fill some online forms every month. 

Pipeliner runs multiple pipelines. Each pipeline is a list of steps that are executed in a row. Pipelines are defined in configuration file.

## Step
Each step gets input data which is modified and then passed to the next step. Step instance is created by using a given class name in `class` field. Constructor parameters are specified in `params` field. If a step fails, pipeliner will repeat the step up to 3 times. If step fails after 3 retries, pipeliner will try run whole pipeline again. 

# Configuration
Pipeliner uses `json` configuration which defines pipelines to be run. Each pipeline consists of multiple steps which are performed one by one. Pipelines can be scheduled by providing crontab-like format schedule in `schedule` field. 

Example configuration: 
```json
{
  "custom_steps": "../custom_steps/",
  "pipelines": [
    {
      "name": "Notify me when new blog post is published",
      "schedule": "* * * * *",
      "steps": [
        {
          "class": "HttpDownload",
          "params": {
            "url": "http://www.example.com/",
            "headers": {}
          }
        },
        {
          "class": "GetHtmlElementText",
          "params": {
            "element_xpath": "(//*[@class=\"post-title\"])[1]/a"
          }
        },
        {
          "class": "CompareWithPrevious",
          "params": {
            "when_same": {
              "class": "DoNothing"
            },
            "when_different": {
              "class": "SendEmailSsl",
              "params": {
                "smtp_host": "smtp.doe.com",
                "smtp_port": 465,
                "login": "john@doe.com",
                "password": "$3cr37",
                "from_email": "john@doe.com",
                "to_email": "sally@doe.com",
                "subject": "Something important happened!"
              }
            }
          }
        }
      ]
    }
  ]
}
```

By providing this configuration, pipeliner will download `http://www.example.com/`. Downloaded content is then passed into the next step which finds `html` element by `(//*[@class=\"post-title\"])[1]/a` XPath and passes content of the element into next step where the element content is compared with previous version from previous run. Lastly, email is sent to john@doe.com if the element content is different.

# Make your wife happy (or angry)
Example configuration to make your wife happy. Or angry if she knows you.
```json
{
  "custom_steps": "../custom_steps/",
  "pipelines": [
    {
      "name": "Make my wife happy",
      "schedule": "*/15 9-14 * * 1-5",
      "steps": [
        {
          "class": "PickRandomText",
          "params": {
            "choices": [
              "I love you my sweetheart",
              "You are the best! :-*",
              "Have a great day honey <3",
              "Hi <3",
              "What would you like me to cook today? :)"
            ]
          }
        },
        {
          "class": "SendMessageFb",
          "params": {
            "login": "john@doe.com",
            "password": "s3cr37pa$$",
            "to_user_name": "Alison Doe"
          }
        }
      ]
    }
  ]
}
```

# How to run
1. Install requirements: `pip install -r requirements.txt`
2. Create a configuration file
3. Run pipeliner `python -m pipeliner /etc/pipeliner/my_config.json`

# Custom steps 
Pipeliner can use custom steps. Just add path to a package with custom steps and use their class names in the configuration file.
```json
{
  "custom_steps": "../custom_steps/",
  "pipelines": [...]
}
```
