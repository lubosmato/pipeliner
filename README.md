# Pipeliner
Pipeliner can do several anoying repetitive tasks for you. For example you want to get an email when a certain blog publishes a new article. Or imagine you must fill some online forms every month. 

# Configuration
Pipeliner uses `json` configuration which defines pipelines to be run. Pipeline consists of multiple steps which are performed one by one. Pipelines can be scheduled by providing crontab-like format schedule in `schedule` field. 

## Step
Each step gets input data which are modified and then passed to the next step. Chain of responsibility pattern is applied. Step instance is created by using a given class name in `class` field. Constructor parameters are specified in `params` field.

By providing this configuration, pipeliner will download `http://www.example.com/`. Downloaded content is then passed into the next step which finds `html` element by `(//*[@class=\"post-title\"])[1]/a` XPath and passes content of the element into next step where the element content is compared with previous version from previous run. Lastly email is sent to john@doe.com if the element content is different.
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
              "class": "SendEmail",
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

# How to run
1. Create a configuration file
2. Run pipeliner `python -m pipeliner /etc/pipeliner/my_config.json`


# Custom steps 
Pipeliner can use custom steps. Just add path to a package with custom steps and use their class names in the configuration file.
```json
{
  "custom_steps": "../custom_steps/",
  "pipelines": [...]
}
```
