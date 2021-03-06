from nicfit.command import Command as BaseCommand
from nicfit.command import CommandError                             # noqa: F401


class Command(BaseCommand):
    """Base class for MishMash commands."""

    def run(self, args, config):
        from . import database

        self.config = config

        (self.db_engine,
         SessionMaker,
         self.db_conn) = database.init(self.config.db_url)

        self.db_session = SessionMaker()

        try:
            retval = super().run(args)
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
        finally:
            self.db_session.close()

        return retval
