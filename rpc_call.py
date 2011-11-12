# -*- coding: utf-8 -*-

# Authorization
AUTH1 = "<auth1/>\n\003"
AUTH2 = "<auth2/>\n" \
        "<nonce_hash>%s</nonce_hash>\n\003"

# Direct RPC
GET_STATE            = "<get_state/>\n"
GET_FILE_TRANSFERS   = "<get_file_transfers/>"
GET_PROJECT_STATUS   = "<get_project_status/>"
GET_DISK_USAGE       = "<get_disk_usage/>\n"
GET_STATISTICS       = "<get_statistics/>\n"
GET_RESULTS          = "<get_results/>"
NETWORK_QUERY        = "<network_query/>\n"
NETWORK_AVAILABLE    = "<network_available/>\n"
GET_RUN_MODE         = "<get_run_mode/>\n"
GET_NETWORK_MODE     = "<get_network_mode/>\n"
GET_SCREENSAVER_MODE = "<get_screensaver_mode/>\n"
RUN_BENCHMARKS       = "<run_benchmarks/>\n"
GET_PROXY_SETTINGS   = "<get_proxy_settings/>\n"
GET_HOST_INFO        = "<get_host_info/>\n"
QUIT                 = "<quit/>\n"

# Template RPC
RUN_MODE_ALWAYS    = "<always/>\n" # BOINC uses symbol constant 0
RUN_MODE_NEVER     = "<never/>\n"  # BOINC uses symbol constant 1
RUN_MODE_AUTO      = "<auto/>\n"   # BOINC uses symbol constant 2

SET_RUN_MODE         = "<set_run_mode>\n%s\n</set_run_mode>\n"
SET_NETWORK_MODE     = "<set_network_mode>\n%s\n</set_network_mode>\n"
SET_SCREENSAVER_MODE = "<set_screensaver_mode>\n" \
                       "%s\n" \
                       "<blank_time>%f</blank_time>\n" \
                       "</set_screensaver_mode>\n"
GET_MESSAGES         = "<get_messages>\n" \
                       "<seqno>%d</seqno>\n" \
                       "</get_messages>\n"
GET_PROJECT_CONFIG   = "<get_project_config>\n" \
                       "<url>%s</url>\n" \
                       "</get_project_config>\n"

# PROJECT RPC has two arguments:
#   1. project url
#   2. operation: reset, detach, update, nomorework, allowmorework
# Each operation is associated with an XML tag
#   reset:         project_reset
#   detach:        project_detach
#   update:        project_update
#   nomorework:    project_nomorework
#   allowmorework: project_allowmorework
#
PROJECT_RESET         = "project_reset"
PROJECT_DETACH        = "project_detach"
PROJECT_UPDATE        = "project_update"
PROJECT_NOMOREWORK    = "project_nomorework"
PROJECT_ALLOWMOREWORK = "project_allowmorework"
PROJECT = \
"<%s>\n" \
"   <project_url>%s</project_url>\n" \
"</%s>\n"

# File transfer RPC has three arguments:
#   1. operations: retry | abort
#   2. project url
#   3. file name
# Each operation is associated with an XML tag
#   retry: retry_file_transfer
#   abort: abort_file_transfer
#
FILE_TRANSFER = \
"<%s>\n" \
"   <project_url>%s</project_url>\n" \
"   <filename>%s</filename>\n" \
"</%s>\n"

# Result RPC has three arguments:
#   1. project url
#   2. resutl's name
#   3. operations: suspend | resume | abort | graphics_window | graphics_fullscreen
# Each operation is associated with an XML tag
#   suspend: suspend_result
#   abort:   abort_result
#   resume:  resume_result
# Particularly,
#   For graphics_window or graphics_fullscreen, the caller should use RESULT_SHOW_GRAPHICS rpc command.
#   If it is graphics_fullscreen, the last %s should be replaced by <full_screen/> or an empty string.
#
FULL_SCREEN = "<full_screen/>\n"
SUSPEND_RESULT = "suspend_result"
ABORT_RESULT   = "abort_result"
RESUME_RESULT  = "resume_result"
RESULT = "<%s>\n" \
         "   <project_url>%s</project_url>\n" \
         "   <name>%s</name>\n" \
         "</%s>\n"
RESULT_SHOW_GRAPHICS = "<result_show_graphics>\n" \
                       "   <project_url>%s</project_url>\n" \
                       "   <result_name>%s</result_name>\n" \
                       "%s" \
                       "</result_show_graphics>\n"
