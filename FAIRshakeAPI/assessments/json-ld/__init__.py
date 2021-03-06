import extruct
import requests
from w3lib.html import get_base_url
from django.conf import settings
from objectpath import Tree

def bind(func, *args, **kwargs):
  def func_wrapper(*_args, **_kwargs):
    return func(*args, *_args, **kwargs, **_kwargs)
  return func_wrapper

def get_json_ld_attr(tree, attrs):
  def get_json_ld_attr_inner():
    for attr in attrs:
      attr_split = attr.split('.')
      # this prefix works for the following syntaxes:
      #  { @context: "http://schema.org", "@type": {attr_type}, {attr_val}: ... }
      #  { @context: "https://schema.org", "@type": [{attr_type}], {attr_val}: ... }
      #  { @context: ["https://schema.org"], "@type": {attr_type}, {attr_val}: ... }
      #  { @context: ["https://schema.org"], "@type": [{attr_type}], {attr_val}: ... }
      for result in tree.execute(
        '$..*["http://schema.org" in @.@context or "https://schema.org" in @.@context]..*[{attr_type} in @.@type].{attr_val}'.format(
          attr_type=attr_split[0],
          attr_val='.'.join(attr_split[1:]),
        )
      ):
        yield str(result)
  return ' '.join(get_json_ld_attr_inner())

to_schema = {
  # 'target:title': [
  # 'WebSite.name', # Thing
  # ],
  'metric:60': [
    'WebSite.name', # Thing
  ],
  # 'target:description': [
  # 'WebSite.description', # Thing
  # ],
  'metric:63': [
    'WebSite.description', # Thing
    'DataCatalog.description',
    'Dataset.description',
  ],
  'metric:21': [
    'DataCatalog.@id',
    'Dataset.@id',
    'DataCatalog.identifier',
    'Dataset.identifier',
  ],
  'metric:29': [
    'WebSite.license', # CreativeWork
    'DataCatalog.license',
    'Dataset.license',
  ],
  'metric:27': [
    'ContactPoint.email',
    'ContactPoint.faxNumber',
    'ContactPoint.telephone',
    'ContactPoint.url',
    'Organization.address',
    'Organization.email',
    'Organization.faxNumber',
    'Organization.telephone',
    'Person.address',
    'Person.email',
    'Person.faxNumber',
    'Person.telephone',
  ],
  'metric:38': [
    'WebSite.version', # CreativeWork
    'DataCatalog.version',
    'Dataset.version',
  ],
  # 'target:image': [
  # 'WebSite.image', # Thing
  # ],
  # 'target:type': [
  # 'WebSite.mainEntity', # CreativeWork
  # ],
  # 'target:tags': [
  # 'WebSite.keywords', # CreativeWork
  # ],
  'metric:77': [
    'WebSite.isAccessibleForFree', # CreativeWork
    'DataCatalog.isAccessibleForFree', # CreativeWork
    'Dataset.isAccessibleForFree', # CreativeWork
  ],
  'metric:36': [
    'WebSite.citation', # CreativeWork
    'DataCatalog.citation', # CreativeWork
    'Dataset.citation', # CreativeWork
  ],
  'metric:25': [
    'Dataset.url', # CreativeWork
  ],
}

class Assessment:
  inputs = [
    'target:url',
  ]
  outputs = [
    'metric:30',
  ] + list(to_schema.keys())

  @classmethod
  def perform(kls, inputs):
    urls = inputs['target:url']
    for url in urls:
      try:
        r = requests.get(url, timeout=1)
        base_url = get_base_url(r.text, r.url)
        data = extruct.extract(r.text, base_url=base_url, syntaxes=['json-ld'])['json-ld']
        tree = Tree(data)
        break
      except:
        data = None

    return dict(
      **{
        'metric:30': {
          'answer': 1.0 if data else 0.0,
          'comment': 'jsonld was found and properly parsed' if data else 'jsonld could not be parsed',
        },
      },
      **{
        key: {
          'answer': 1.0 if attr else 0.0,
          'comment': attr if attr else 'json-ld %s not found' % (' '.join(to_schema[key])),
        } if key.startswith('metric:') else attr
        for key, attr in zip(
          to_schema.keys(),
          map(
            bind(get_json_ld_attr, tree),
            to_schema.values()
          )
        )
      } if data else {key: {} for key in to_schema.keys()}
    )
