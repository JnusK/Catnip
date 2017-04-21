# Catnip
Project for DSGN 384 2016-2017
This app is a priority based time management app targeted at Northwestern freshmen to help them manage their time efficiently.
The goal is to create an app that has a priority based time management function as the main feature.

Included features:
  - Canvas integration to pull assignments (Limited due to some issues)
  - CAESAR integration for class schedule

Additional features to be included are as below:
  - NU Dining Integration
  - Messaging Function

Tasks to be done:
  - Build Priority View
  - Build List View
  - Build Calendar View (In progress)
  - Convert code to OOP (In progress)
  - Build persistent data storage
  - Pull Class Schedule from CAESAR everytime courses change on Canvas
  - Pull Class Assignments from Canvas each time app start up or manual refresh or every week
  - Add ability for manual entry of tasks
  
  
  
  
  
  CAESAR course API documentation: http://developer.asg.northwestern.edu/docs/

Canvas Course Object------------------------------------------------------------------------------    
 {
	"id": 18760000000025827,
	"name": "2015FA_EECS_111-0_SEC20_AND_395-0_SEC45",
	"account_id": 18760000000000212,
	"start_at": "2015-08-31T05:00:00Z",
	"grading_standard_id": null,
	"is_public": false,
	"course_code": "2015FA_EECS_111-0_SEC20_AND_395-0_SEC45",
	"default_view": "feed",
	"root_account_id": 18760000000000001,
	"enrollment_term_id": 18760000000000105,
	"end_at": "2015-12-26T06:00:00Z",
	"public_syllabus": false,
	"public_syllabus_to_auth": false,
	"storage_quota_mb": 500,
	"is_public_to_auth_users": false,
	"apply_assignment_group_weights": true,
	"calendar": {
		"ics": "https://canvas.instructure.com/feeds/calendars/course_dPrOcHw0m2IbaAga6CZBjcWDFubPiwuDGJopdILg.ics"
	},
	"time_zone": "America/Chicago",
	"enrollments": [{
		"type": "student",
		"role": "StudentEnrollment",
		"role_id": 821,
		"user_id": 18760000000011486,
		"enrollment_state": "active"
	}],
	"hide_final_grades": false,
	"workflow_state": "available",
	"restrict_enrollments_to_course_dates": true
}

Canvas Assignment Object------------------------------------------------------------------------------

  {\
  	"id\":18760000000339955,\
  	"description\":\"\",\
  	"due_at\":null,\
  	"unlock_at\":null,\
  	"lock_at\":null,\
  	"points_possible\":0.0,\
  	"grading_type\":\"points\",\
  	"assignment_group_id\":18760000000101670,\
  	"grading_standard_id\":null,\
  	"created_at\":      \"2017-04-14T15:14:34      Z\",\
  	"updated_at\":      \"2017-04-15T20:51:38      Z\",\
  	"peer_reviews\":false,\
  	"automatic_peer_reviews\":false,\
  	"position\":1,\
  	"grade_group_students_individually\":false,\
  	"anonymous_peer_reviews\":false,\
  	"group_category_id\":null,\
  	"post_to_sis\":false,\
  	"moderated_grading\":false,\
  	"omit_from_final_grade\":false,\
  	"intra_group_peer_reviews\":false,\
  	"secure_params\":\"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsdGlfYXNzaWdubWVudF9pZCI6ImJlNGVjOWFkLTRjOTEtNDlmMy1iNjEwLTI5NWNjNTU0ODc2YiJ9.k589xs7ABSUAJEFpczvzty8qIiWKTby5bvfFW7OwwPA\",\
  	"course_id\":18760000000056390,\
  	"name\":\"Paper Review #1\",\
  	"submission_types\":[  \
  	"online_upload\"
  ], \"has_submitted_submissions\":true,\
  "due_date_required\":false,\
  "max_name_length\":255,\
  "in_closed_grading_period\":false,\
  "is_quiz_assignment\":false,\
  "muted\":false,\
  "html_url\":      \"https://canvas.instructure.com/courses/18760000000056390/assignments/1876~339955\",\
  "published\":true,\
  "only_visible_to_overrides\":false,\
  "locked_for_user\":false,\
  "submissions_download_url\":      \"https://canvas.instructure.com/courses/1876~56390/assignments/1876~339955/submissions?zip=1\"
  }


