# -*- coding: utf-8 -*-

from core import *
from display import *
from argv_visitor import ARGV_VISITOR
from definition import GUI_RPC_AUTH_CONFIG

USAGE = "usage: boinc_shell.py [--project | --result | --help]"

def can_do_task():
    handler = shell_core()
    try:
        handler.prepare()
        if handler.authorize():
            return handler
        else:
            print "unauthorized"
            return None
    except IOError:
        print "Cannot read config file."
        return None
    except:
        print "Cannot connect to BOINC."
        return None

def end_task(handler):
    if handler: handler.done()

def main():
    av = ARGV_VISITOR()

    s = av.next_argv()
    if s == "--help":
        print USAGE
    elif s == "--boinc_dir":
        s = av.next_argv()
        if s == None:
            print "Invalid argument. " \
                  "There should be a directory path " \
                  "following --boinc_dir."
        else:
            import os.path
            if not os.path.exists(s):
                print "Cannot find the directory."
            else:
                if not os.path.exists(os.path.join(s, GUI_RPC_AUTH_CONFIG)):
                    print "Cannot read BOINC's configuration.\nPlease check " \
                          "whether the BOINC client software is installed " \
                          "correctly."
                else:
                    # copy BOINC's config file to current directory
                    import shutil
                    try:
                        shutil.copyfile(
                            os.path.join(s, GUI_RPC_AUTH_CONFIG),
                            GUI_RPC_AUTH_CONFIG)
                    except IOError:
                        print "Cannot create file under current directory."
    elif s == "--project":
        project_name = av.next_argv()
        if project_name == None:
            # display projects directly
            handler = can_do_task()
            if handler:
                display_projects(handler.get_projects())
                end_task(handler)
        else:
            operation = av.next_argv()
            if operation == None or not (operation in ("reset", "update", "detach", "nomorework", "allowmorework")):
                print "Invalid argument. There should be an operation " \
                      "following project name."
                print "They may be reset, update, detach, nomorework, " \
                      "or allowmorework."
            else:
                # do --project operation
                handler = can_do_task()
                if handler:
                    project = handler.get_projects().lookup_project(project_name)
                    if project:
                        handler.set_project(project, operation)
                    else:
                        print "Cannot find project %s" % (project_name)

                    end_task(handler)
    elif s == "--result":
        project_name = av.next_argv()
        if project_name == None:
            handler = can_do_task()
            if handler:
                display_results(handler.get_results())
                end_task(handler)
        else:
            result_name = av.next_argv()
            if result_name == None:
                print "Invalid argument. There should be a result name " \
                      "following the project name."
            else:
                operation = av.next_argv()
                if operation == None or not (operation in ("suspend", "abort", "resume")):
                    print "Invalid argument. There should be an operation " \
                          "following result name."
                    print "They may be suspend, abort, or resume."
                else:
                    # do --result operation
                    handler = can_do_task()
                    if handler:
                        project = handler.get_projects().lookup_project(project_name)
                        result = handler.get_results().lookup_result(result_name)
                        if project and result:
                            handler.set_result(project, result, operation)
                        if not project:
                            print "Cannot find project %s" % (project_name)
                        if not result:
                            print "Cannot find result %s" % (result_name)

                        end_task(handler)
    elif s == "--get_file_transfers":
        handler = can_do_task()
        if handler:
            print handler.get_file_transfers()
            end_task(handler)
    else:
        # display projects and results
        handler = can_do_task()
        if handler:
            display_projects(handler.get_projects())
            display_results(handler.get_results())

            end_task(handler)

if __name__ == "__main__":
    main()
