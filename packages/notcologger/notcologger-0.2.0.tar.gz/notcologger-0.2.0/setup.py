# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notcologger']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['test = scripts:test']}

setup_kwargs = {
    'name': 'notcologger',
    'version': '0.2.0',
    'description': 'Not CO Logger, a cloud logging library.',
    'long_description': '# Not-co-logger\n\nNot-co-logger is a simple Python library to help log things to stdout in a \nspecific JSON format. It is inspired by the checkout-logger TypeScript \nlibrary (https://github.com/CheckoutFinland/checkout-logger).\n\n## How to use\n\nThis guide is short and in need of much verbosity.\n\nThe idea behind this library is that typically in a complex cloud environment it makes ones life much easier if apps log to stdout in a consistent JSON format. This library implements in a pretty simple form some practices that have been found useful.\n\nLogSpan(requestId) creates a logspan object, which has error, warn, info and debug methods to log varying levels of messages. All messages have a type (for example "lambda.handler.start"), message, log group (for example technical or session), and optionally user (could be IP or user id) and meta (free form object).\n\nA good logtype is unique or at least easily greppable. We suggest naming them hierarchically, for example \'component.module.subtask\' or something like that. A logtype should be informative but not overly rigid or verbose. Message is the typical human readable part of an event. Meta should be understood as a grab bag object for any additional fields that would be considered useful for the particular log event. For example a HTTP request log event could have the requested path included in the meta object.\n\nAll log rows are bound together by the requestId when logging them. Timestamps are automatically added.\n\n## Levels\n\nThese are suggested guidelines for log levels:\n\n* Error: The system has run into a fatal exception that requires attention from admins.\n* Warning: Something went wrong, but admins do not need to be urgently alerted.\n* Info: Normal logging.\n* Debug: General developer friendly spam that is wanted in the logs for common "what the hell just happened" type of solving.\n\n## Suggested group\n\nHere are some groups that have been found to be useful:\n\n* request: Incoming requests\n* response: Outgoing responses\n* session: Events related to an active session\n* technical: Events related to some technical state or issues\n\n## ExceptionSpan\n\nWhen you need to log an error but only when an exception is raised, you can use ExceptionSpan context manager:\n\n```\n    with ExceptionSpan(\'mylog.problem\', \'Doing something fails\') as log:\n        do_something_that_fails()\n        log.info(\'mylog.success\', \'It worked!\', \'technical\')\n```\n\nIf `do_something_that_fails()` fails and raises an exception, the ExceptionSpan logs an error. If the call succeeds, the optional log.info() is called. Note that ExceptionSpan does not catch the exception.\n\n\n',
    'author': 'Juha-Matti Tapio',
    'author_email': 'jmtapio@verkkotelakka.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jmtapio/not-co-logger',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
