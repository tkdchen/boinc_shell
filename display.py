# -*- coding: utf-8 -*-

from definition import *

def display_projects(ps):
    for p in ps.projects:
        print "--- %s ---" % (p.project_name)
        print "  project url: %s\n" \
              "  user_name: %s\n" \
              "  team name: %s\n" \
              "  user total credit: %f\n" \
              "  user expavg credit: %f\n" \
              "  host total credit: %f\n" \
              "  host expavg credit: %f\n" % (
                  p.master_url,
                  p.user_name, p.team_name,
                  p.user_total_credit,
                  p.user_expavg_credit,
                  p.host_total_credit,
                  p.host_expavg_credit)
        if p.suspended_via_gui:
            print "suspended by user"
        if p.dont_request_more_work:
            print "project does not request more work."
        if p.gui_urls.ifteam():
            gu = p.gui_urls.team
            print "%s" % (gu.name)
            print "  description: %s\n" \
                  "  url: %s\n" % (gu.description, gu.url)

def display_results(rs):
    n = 0
    for r in rs.results:
        n += 1
        print "--- Result (%d) ---" % (n)
        print "  name: %s\n" \
              "  work unit name: %s\n" \
              "  project url: %s\n" \
              "  report deadline: %f" % (
                  r.name, r.wu_name,
                  r.project_url,
                  r.report_deadline)
        if r.is_active():
            print "  current cpu time: %f\n" \
                  "  fraction done: %.2f%%" % (
                      r.current_cpu_time, r.fraction_done * 100)
            if r.supports_graphics:
                print "  supports graphics"
            else:
                print "  does not support graphics"
        else:
            print "  final cpu time: %f" % (r.final_cpu_time)
        print "  state:",
        if r.state == RESULT_NEW:
            print "New"
        elif r.state == RESULT_FILES_DOWNLOADING:
            if r.ready_to_report:
                print "Download failed"
            else:
                print "Downloading"
        elif r.state == RESULT_FILES_DOWNLOADED:
            if r.suspended_via_gui:
                print "suspended by user"
            elif r.aborted_via_gui:
                print "aborted by user"
            elif r.is_active:
                if r.scheduler_state == CPU_SCHED_SCHEDULED:
                    print "Running"
                elif r.scheduler_state == CPU_SCHED_PREEMPTED:
                    print "Preempted"
                elif r.scheduler_state == CPU_SCHED_UNINITIALIZED:
                    print "Ready to run"
            else:
                print "Ready to run"
        elif r.state == RESULT_COMPUTE_ERROR:
            if r.aborted_via_gui or r.exit_status == ERR_ABORTED_VIA_GUI:
                print "Aborted by user"
            else:
                print "Computation error"
        elif r.state == RESULT_FILES_UPLOADING:
            if r.ready_to_report:
                print "Uploading failed"
            else:
                print "Uploading"
        else:
            if r.got_server_ack:
                print "Acknowledged"
            elif r.ready_to_report:
                print "ready to report"
            else:
                print "Error: invalid state %d" % (r.state)
        print # just make a enter
