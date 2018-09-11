import uuid
from versions.models import Versionable, VersionManager, VersionedQuerySet
from versions.fields import VersionedForeignKey, VersionedManyToManyField
from .fields import CustomUUIDField

class VersionedQuerySetEx(VersionedQuerySet):
  def _set_item_querytime(self, item, type_check=False):
    """
    Sets the time for which the query was made on the resulting item
    :param item: an item of type Versionable
    :param type_check: Check the item to be a Versionable
    :return: Returns the item itself with the time set
    """
    if isinstance(item, VersionedQuerySet) or isinstance(item, VersionedQuerySetEx):
      item.querytime = self.querytime
    else: #if isinstance(item, Versionable) or isinstance(item, VersionableEx):
      # Note: This will fall back to a `fake` model during django migrations, hence the else
      item._querytime = self.querytime
    return item

class VersionManagerEx(VersionManager):
  use_in_migrations = True

  def get_queryset(self):
    qs = VersionedQuerySetEx(self.model, using=self._db)
    if hasattr(self, 'instance') and hasattr(self.instance, '_querytime'):
        qs.querytime = self.instance._querytime
    return qs

  def create(*args, **kwargs):
    res = VersionManager.create(*args, **kwargs)
    res.is_current = VersionableEx.is_current
    res.querytime = VersionableEx.is_current
    return res

class VersionableEx(Versionable):
  id = CustomUUIDField(default=uuid.uuid4, primary_key=True)
  identity = CustomUUIDField()

  objects = VersionManagerEx()

  class Meta:
    abstract = True
