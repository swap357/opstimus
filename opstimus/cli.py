import argparse

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Ops CLI tool')
        subparsers = self.parser.add_subparsers(dest='command')

        # Create subparser for 'create' command
        create_parser = subparsers.add_parser('new', help='Create a new task using natural language query')
        create_parser.add_argument('query', help='user query to create task')

        # Create subparser for 'run' command
        run_parser = subparsers.add_parser('run', help='Run a task')
        run_parser.add_argument('task', help='The task to run')

        # Create subparser for 'list' command
        list_parser = subparsers.add_parser('ls', help='List all tasks')

        # Create subparser for 'delete' command
        delete_parser = subparsers.add_parser('rm', help='Delete a task')
        delete_parser.add_argument('task', help='The task to delete')

        # Create subparser for 'update' command
        update_parser = subparsers.add_parser('update', help='Update a task')
        update_parser.add_argument('task', help='The task to update')

        # Create subparser for 'view' command
        view_parser = subparsers.add_parser('cat', help='View a task')
        view_parser.add_argument('task', help='The task to view')

        # Create subparser for 'help' command
        help_parser = subparsers.add_parser('help', help='Show help information')

    def parse_args(self):
        args = self.parser.parse_args() or argparse.Namespace()
        return args
