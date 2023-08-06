# WebCase message sender

Message sender to different channels.

## Installation

```sh
pip install wc-django-envoyer
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'wcd_envoyer',
]

WCD_ENVOYER = {
  # Channels list, that will be available in admin interface to message
  # create templates.
  'CHANNELS': [
    {
      # Unique channel key.
      'key': 'console',
      'verbose_name': 'Console',
      # Messaging backend class.
      # Console backend here is a simple message printing backend:
      'backend': 'wcd_envoyer.channels.backends.console.ConsoleBackend',
      'options': {
        # Options that backend receives on initialization.
        # Basic ones are:
        # Actual recipients data resolver for a specific case:
        'recipient_resolver': lambda x: x,
        # Form for additional in-admin backend configuration options.
        'config_form_class': 'wcd_envoyer.channels.forms.BaseConfigForm',
        # In-admin form for template config.
        'template_form_class': 'wcd_envoyer.channels.forms.BaseTemplateForm',
        # Custom string template renderer.
        'template_renderer': 'wcd_envoyer.channels.renderers.django_template_renderer',
        # Separate class that is responsible for messages data transformations.
        'messages_maker_class': 'wcd_envoyer.channels.backend.MessagesMaker',
      }
    },
  ],
  'EVENTS': [
    {
      # Unique event key.
      'key': 'something-happened',
      # Event's verbose name that will be displayed in admin.
      'verbose_name': 'Something happened event',
      # List of variables available on template generation.
      'context': [
        (
          # Key
          'when',
          # Verbose name.
          'When',
          # Additional variable description
          'Time when something happened.'
        ),
        # Variable can be defined as a simple string key:
        'what',
        # Or this could be tuple with only 2 parameters
        ('other', 'Other'),
      ],
  }
  ],
  # JSON encoder class for in-lib postgres json fields:
  'JSON_ENCODER': 'django.core.serializers.json.DjangoJSONEncoder',
}
```

**Builtin backends:**

- `wcd_envoyer.channels.backends.console.ConsoleBackend` - Simple backend to send messages to console. For debug purposes.
- `wcd_envoyer.channels.backends.django_sendmail.SendMailBackend` - Backend with django's email sending mechanics underneath.

Events and Channels can be registered in special auto-importable `envoyer.py` app submodule.

`envoyer.py`
```python
from django.utils.translation import pgettext_lazy

from wcd_envoyer import events, channels


# Events is better to register here. Because it's more related to
# particular app, not project itself.
events.registry.add({
  'key': 'app-event',
  'verbose_name': 'App event',
  'context': ['var1', 'var2'],
})

# But channels is other case. Better describe them in `settings.py`
channels.registry.add({
  'key': 'sms',
  'verbose_name': 'Sms sender',
  'backend': 'app.envoyer.backends.SMSBackend',
})
```

## Usage

Simple shortcut usage is `send` shortcut.

```python
from wcd_envoyer.shortcuts import send, default_sender

send(
  # Event name
  'app-event',
  # Recipients list.
  # Recipient object is a dict with any key-values, from which different
  # backends will get data they need.
  [
    # This recipient will be used only by sms, or phone call backend.
    {'phone': '+0000000000'},
    # This will be user by email sending backend.
    {'email': 'some@email.com'},
    # And both backends will send message to recipient like that.
    {'phone': '+0000000000', 'email': 'some@email.com'},
  ],
  # Data object, what will be used to render Message.
  # It could be dict with any data.
  # For event probably there will be data for event's context.
  {
    'var1': 'data',
    'var2': 'data',
    # If you need to send messages with specific language, you may add it here:
    'language': 'en',
    # And also any other backend-specific options could be passed to context.
    # ...
  },
  # You may additionally limit channels that message will be send.
  channels=['sms'],
  # Or. None - all channels possible.
  channels=None,
  # Optional parameter, with which you may change sender instance, to your
  # custom one.
  sender=default_sender,
)
```

### Signals

App has internal signals, that you may use to take actions after messages were sended.

- `wcd_envoyer.signals.messages_sent` - Messages sent signal.
- `wcd_envoyer.signals.messages_sent_succeeded` - Signal for messages that were successfully sent.
- `wcd_envoyer.signals.messages_sent_failed` - Signal that fires if any messages were failed to send.

### Celery

Celery support is provided via `wcd_envoyer.contrib.celery` package.

`tasks.py`
```python
from .celery import app

from wcd_envoyer.contrib.celery.shortcuts import task, make_task
from wcd_envoyer.shortcuts import send


# Decorator for task creation is the easiest way to make things work.
@task(app)
def sending_task_1(result, context):
  # Callback for task will run AFTER all messages sending happened.
  succeeded, failed = result
  # - succeeded - List of successfully sent messages.
  # - failed - List of messages that we failed to send.
  # And context - is the same context that were passed on `send`.

# OR

# If you do not need any callback and default signals is enough then just
# create task:
sending_task_2 = make_task(app)

created_task = (sending_task_1 or sending_task2)

# An now, after you've created task and sender you may easily send messages:
send(
  'app-event', [{'email': 'some@email.com'}], {'var': 'data'},
  # You may use sender in initial shortcut:
  sender=created_task.sender,
)
# OR
# Execute the same `send` from task:
created_task.send(
  'app-event', [{'email': 'some@email.com'}], {'var': 'data'},
)
# OR
# Just use created sender directly:
created_task.sender.send(...)
```

To use celery sender in admin interface instead of the "straight" one you should change sender in `Message` admin class:

```python
from wcd_envoyer.admin import MessageAdmin

# Looking hacky, but you you need - just inherit from `MessageAdmin`
# and re-register admin for `Message` model.
MessageAdmin.messages_sender = created_task.sender
```

### Error tracking

You can track failed messages with signals. Or there is a simple connector for `px-django-actions-tracker` lib. Just add `'wcd_envoyer.contrib.pxd_actions_tracker'` to `INSTALLED_APPS`.
