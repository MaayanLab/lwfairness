from django.db.models import Q
from FAIRshakeAPI import models
from functools import reduce

class SearchVector:
  def __init__(self, qs=None):
    self.queryset = qs or self.get_model().objects.filter(id__isnull=False)

  def get_model(self):
    return self.model
  
  def get_filters(self):
    return getattr(self, 'filters', [])

  def get_queryset(self):
    return self.queryset

  def query(self, q):
    return self.get_queryset().filter(
      reduce(
        lambda F, f, q=q: (F|f(q)) if F is not None else f(q),
        self.get_filters(),
        None,
      )
    ).order_by(*self.get_model()._meta.ordering).distinct()

class IdentifiableSearchVector(SearchVector):
  filters = [
    lambda q: Q(title__search=q),
    lambda q: Q(url__url_similar=q),
    lambda q: Q(description__search=q),
    lambda q: Q(tags__search=q),
    lambda q: Q(authors__first_name__istartswith=q),
    lambda q: Q(authors__last_name__istartswith=q),
    lambda q: Q(authors__email__istartswith=q),
  ]

class ProjectSearchVector(IdentifiableSearchVector):
  model = models.Project

class DigitalObjectSearchVector(IdentifiableSearchVector):
  model = models.DigitalObject

class RubricSearchVector(IdentifiableSearchVector):
  model = models.Rubric

class MetricSearchVector(IdentifiableSearchVector):
  model = models.Metric
