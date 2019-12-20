# Pipeliner
Pipeliner can do several anoying repetitive tasks for you. For example you want to get an email when a certain blog publishes a new article. Or imagine you must fill some online forms every month. 

# Configuration
Pipeliner uses `json` configuration which defines pipelines to be run. Pipeline consists of multiple steps which are performed one by one. Pipelines can be scheduled by providing crontab-like format schedule in `schedule` field. 

## Step
Each step gets input data which are modified and then passed to the next step. Chain of responsibility pattern is applied. Step instance is created by using a given class name in `class` field. Constructor parameters are specified in `params` field.

By providing this configuration, pipeliner will download file from `http://www.example.com`. Downloaded file is then passed into the next step which finds `html` element by `(//*[@class=\"post-title\"])[1]/a` XPath. In the next step html tags are removed and lastly email is sent to john@doe.com.
```json
{
  "pipelines": [
    {
      "name": "Notify me when new blog post is published",
      "schedule": "* * * * *",
      "steps": [
        {
          "class": "DownloadFile",
          "params": {
            "url": "http://www.example.com/"
          }
        },
        {
          "class": "FindHtmlElement",
          "params": {
            "element_xpath": "(//*[@class=\"post-title\"])[1]/a"
          }
        },
        {
          "class": "RemoveHtmlTags",
        },
        {
          "class": "SendEmail",
          "params": {
            "to": "john@doe.com"
          }
        }
      ]
    }
  ]
}
```

# Custom steps 
Pipeliner can use custom steps. Just add path to a package with custom steps and use their class names in the configuration file.
```json
{
  "custom_steps": "../custom_steps/",
  "pipelines": [...]
}
```
