import canvaslms.cli
import canvaslms.cli.assignments as assignments
import canvaslms.cli.courses as courses
import canvaslms.cli.submissions as submissions
import canvaslms.hacks.canvasapi

import argparse
import csv
import canvasapi.submission
import datetime as dt
import importlib
import importlib.machinery
import importlib.util
import os
import pathlib
import re
import sys

def results_command(config, canvas, args):
  output = csv.writer(sys.stdout, delimiter=args.delimiter)

  assignments_list = assignments.process_assignment_option(canvas, args)

  if args.assignment_group != "":
    results = summarize_assignment_groups(canvas, args)
  else:
    results = summarize_assignments(canvas, args)

  for result in results:
    if not args.include_Fs and result[3][0] == "F":
      continue
    output.writerow(result)
def summarize_assignments(canvas, args):
  """
  Turn submissions into results:
  - canvas is a Canvas object,
  - args is the command-line arguments, as parsed by argparse.
  """

  courses_list = courses.process_course_option(canvas, args)

  users_list = []
  for course in courses_list:
    for user in course.get_users(enrollment_type=["student"]):
      users_list.append(user)

  assignments_list = assignments.process_assignment_option(canvas, args)
  submissions_list = submissions.filter_submissions(
    submissions.list_submissions(assignments_list,
                                 include=["submission_history"]),
    users_list)

  for submission in submissions_list:
    if submission.grade is not None:
      yield [
        submission.assignment.course.course_code,
        submission.assignment.name,
        submission.user.integration_id,
        submission.grade,
        round_to_day(submission.submitted_at or submission.graded_at),
        *all_graders(submission)
      ]
def round_to_day(timestamp):
  """
  Takes a Canvas timestamp and returns the corresponding datetime.date object.
  """
  return dt.date.fromisoformat(timestamp.split("T")[0])
def all_graders(submission):
  """
  Returns a list of everyone who participated in the grading of the submission. 
  I.e. also those who graded previous submissions, when submission history is 
  available.
  """
  graders = []

  for prev_submission in submission.submission_history:
    prev_submission = canvasapi.submission.Submission(
      submission._requester, prev_submission)
    prev_submission.assignment = submission.assignment
    grader = submissions.resolve_grader(prev_submission)
    if grader:
      graders.append(grader)

  return graders
def summarize_assignment_groups(canvas, args):
  """
  Summarize assignment groups into a single grade:
  - canvas is a Canvas object,
  - args is the command-line arguments, as parsed by argparse.
  """

  try:
    summary = importlib.import_module(args.summary_module)
  except ModuleNotFoundError:
    module_path = pathlib.Path.cwd() / args.summary_module
    module = module_path.stem

    try:
      loader = importlib.machinery.SourceFileLoader(
        module, str(module_path))
      spec = importlib.util.spec_from_loader(module, loader)
      summary = importlib.util.module_from_spec(spec)
      loader.exec_module(summary)
    except Exception as err:
      canvaslms.cli.err(1, f"Error loading summary module "
        f"'{args.summary_module}': {err}")

  courses_list = courses.process_course_option(canvas, args)
  all_assignments = list(assignments.process_assignment_option(canvas, args))

  for course in courses_list:
    users_list = list(course.get_users(enrollment_type=["student"]))
    ag_list = assignments.filter_assignment_groups(
      course, args.assignment_group)

    for assignment_group in ag_list:
      assignments_list = list(assignments.filter_assignments_by_group(
        assignment_group, all_assignments))
      for user, grade, grade_date, *graders in summary.summarize_group(
        assignments_list, users_list):
          yield [
            course.course_code,
            assignment_group.name,
            user.integration_id,
            grade,
            grade_date,
            *graders
          ]

def add_command(subp):
  """Adds the results command to argparse parser subp"""
  results_parser = subp.add_parser("results",
      help="Lists results of a course",
      description="""Lists results of a course for export, for instance to the `ladok report` 
                     command. Output format, CSV:

                       <course code> <component code> <student ID> <grade> <grade date> <graders ...>""",
      epilog="""If you specify an assignment group, the results of the assignments in that 
                group will be summarized. You can supply your own function for summarizing 
                grades through the -S option. See `pydoc3 canvaslms.grades` for different 
                options.""")
  results_parser.set_defaults(func=results_command)
  assignments.add_assignment_option(results_parser, ungraded=False)
  default_summary_module = "canvaslms.grades.conjunctavg"
  results_parser.add_argument("-S", "--summary-module",
    required=False, default=default_summary_module,
    help=f"""Name of Python module or file containing module to load with a custom 
             summarization function to summarize assignment groups. The default module is 
             part of the `canvaslms` package: `{default_summary_module}`. This module must 
             contain a function `summarize_group(assignments, users)`, where `assignments` 
             is a list of `canvasapi.assignment.Assignment` objects and `users` is a list of 
             `canvasapi.user.User` objects. The return value must be a list of lists of the 
             form `[user object, grade, grade date, grader 1, grader 2, ...]`.""")
  results_parser.add_argument("-F", "--include-Fs",
    required=False, default=False, action="store_true",
    help="Include failing grades (Fs) in output. By default we only output "
      "A--Es and Ps.")
