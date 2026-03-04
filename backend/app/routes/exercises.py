# # # from fastapi import APIRouter, HTTPException, Depends
# # # from app.schemas import ExerciseSubmit
# # # from app.ai_service import evaluate_text, predict_learning_path
# # # from app.routes.auth import get_current_user
# # # from app.db import db
# # # from bson import ObjectId
# # # import traceback
# # # from datetime import datetime

# # # router = APIRouter()

# # # @router.post('/submit')
# # # async def submit_ex(payload: ExerciseSubmit, user=Depends(get_current_user)):
# # #     try:
# # #         lesson = db['lessons'].find_one({"slug": payload.lesson_id})
# # #         if not lesson:
# # #             raise HTTPException(status_code=404, detail="Lesson not found")

# # #         lesson_title = lesson.get('title', 'Unknown Lesson')
# # #         lesson_desc = lesson.get('description', '')

# # #         ai_response = await evaluate_text(
# # #             user_input=payload.user_input,
# # #             user_level=user.get('level', 'beginner'),
# # #             lesson_context={
# # #                 "lesson_id": payload.lesson_id,
# # #                 "lesson_title": lesson_title,
# # #                 "lesson_description": lesson_desc
# # #             }
# # #         )

# # #         # Save result
# # #         result = {
# # #             'user_email': user['email'],
# # #             'lesson_id': payload.lesson_id,
# # #             'user_input': payload.user_input,
# # #             'evaluation': ai_response,
# # #             'submitted_at': datetime.utcnow(),
# # #             'favorite': False
# # #         }
# # #         db['exercise_results'].insert_one(result)

# # #         # Level progression
# # #         results = list(db['exercise_results'].find({'user_email': user['email']}))
# # #         if len(results) >= 5:
# # #             avg_score = sum(r['evaluation'].get('score', 0) for r in results) / len(results)
# # #             new_level = "beginner"
# # #             if avg_score >= 0.88:
# # #                 new_level = "advanced"
# # #             elif avg_score >= 0.75:
# # #                 new_level = "intermediate"

# # #             if user.get('level') != new_level:
# # #                 db['users'].update_one(
# # #                     {"email": user['email']},
# # #                     {"$set": {"level": new_level}}
# # #                 )

# # #         # Update recommended path
# # #         learning_path = predict_learning_path(results, user.get('level', 'beginner'))
# # #         db['users'].update_one(
# # #             {"email": user['email']},
# # #             {"$set": {"recommended_path": learning_path}}
# # #         )

# # #         return ai_response

# # #     except Exception as e:
# # #         traceback.print_exc()
# # #         raise HTTPException(status_code=502, detail=f"AI evaluation failed: {str(e)}")


# # from fastapi import APIRouter, HTTPException, Depends
# # from app.schemas import ExerciseSubmit
# # from app.services.ai_service import evaluate_text, predict_learning_path
# # from app.routes.auth import get_current_user
# # from app.db import db
# # from datetime import datetime
# # import traceback

# # router = APIRouter()

# # @router.post('/submit')
# # async def submit_ex(payload: ExerciseSubmit, user=Depends(get_current_user)):
# #     try:
# #         lesson = db['lessons'].find_one({"slug": payload.lesson_id})
# #         if not lesson:
# #             raise HTTPException(status_code=404, detail="Lesson not found")

# #         lesson_context = {
# #             "lesson_id": payload.lesson_id,
# #             "lesson_title": lesson.get('title', 'Unknown Lesson'),
# #             "lesson_description": lesson.get('description', ''),
# #             "content": lesson.get('content', {})
# #         }

# #         evaluation = evaluate_text(payload.user_input, lesson_context, user.get('level', 'beginner'))

# #         # Save result
# #         result = {
# #             'user_email': user['email'],
# #             'lesson_id': payload.lesson_id,
# #             'user_input': payload.user_input,
# #             'evaluation': evaluation,
# #             'submitted_at': datetime.utcnow(),
# #             'favorite': False
# #         }
# #         db['exercise_results'].insert_one(result)

# #         # Level progression
# #         results = list(db['exercise_results'].find({'user_email': user['email']}))
# #         if len(results) >= 5:
# #             avg_score = sum(r['evaluation'].get('score', 0) for r in results) / len(results)
# #             new_level = "beginner"
# #             if avg_score >= 0.88:
# #                 new_level = "advanced"
# #             elif avg_score >= 0.75:
# #                 new_level = "intermediate"

# #             if user.get('level') != new_level:
# #                 db['users'].update_one({"email": user['email']}, {"$set": {"level": new_level}})

# #         # Update recommended path
# #         learning_path = predict_learning_path(results, user.get('level', 'beginner'))
# #         db['users'].update_one({"email": user['email']}, {"$set": {"recommended_path": learning_path}})

# #         return evaluation

# #     except Exception as e:
# #         traceback.print_exc()
# #         raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


# from fastapi import APIRouter, HTTPException, Depends
# from app.schemas import ExerciseSubmit
# from app.routes.auth import get_current_user
# from app.db import db
# from datetime import datetime
# import traceback

# router = APIRouter()

# @router.post('/submit')
# async def submit_ex(payload: ExerciseSubmit, user=Depends(get_current_user)):
#     try:
#         lesson = db['lessons'].find_one({"slug": payload.lesson_id})
#         if not lesson:
#             raise HTTPException(status_code=404, detail="Lesson not found")

#         # Save submission as-is
#         result = {
#             'user_email': user['email'],
#             'lesson_id': payload.lesson_id,
#             'user_input': payload.user_input,
#             'submitted_at': datetime.utcnow(),
#             'favorite': False
#         }
#         db['exercise_results'].insert_one(result)

#         # Update recommended path based on weak lessons or incomplete lessons
#         all_results = list(db['exercise_results'].find({'user_email': user['email']}))
#         completed_lessons = [r['lesson_id'] for r in all_results]
#         all_lessons = [l['slug'] for l in db['lessons'].find({})]
#         pending_lessons = [l for l in all_lessons if l not in completed_lessons]

#         db['users'].update_one(
#             {"email": user['email']},
#             {"$set": {"recommended_path": pending_lessons}}
#         )

#         return {"ok": True, "message": "Exercise submitted successfully."}

#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Submission failed: {str(e)}")


from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ExerciseSubmit
from app.routes.auth import get_current_user
from app.db import db
from app.services.ai_service import evaluate_text, summarize_for_recommendation
from app.services.student_metrics import update_user_learning_path
from datetime import datetime
import traceback

router = APIRouter()


@router.post('/submit')
async def submit_ex(payload: ExerciseSubmit, user=Depends(get_current_user)):
    try:
        # Get lesson
        lesson = db['lessons'].find_one({"slug": payload.lesson_id})
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        lesson_context = {
            "lesson_id": payload.lesson_id,
            "lesson_title": lesson.get('title', 'Unknown Lesson'),
            "lesson_description": lesson.get('description', ''),
            "content": lesson.get('content', {})
        }

        # Call AI evaluation (handles fallback internally)
        evaluation = await evaluate_text(payload.user_input, lesson_context, user.get('level', 'beginner'))

        # Save result including evaluation
        result = {
            'user_email': user['email'],
            'lesson_id': payload.lesson_id,
            'user_input': payload.user_input,
            'evaluation': evaluation,
            'submitted_at': datetime.utcnow(),
            'favorite': False
        }
        insert_res = db['exercise_results'].insert_one(result)

        # Update level progression based on recent scores
        results = list(db['exercise_results'].find({'user_email': user['email']}))
        if len(results) >= 5:
            avg_score = sum(r.get('evaluation', {}).get('score', 0) for r in results) / len(results)
            new_level = "beginner"
            if avg_score >= 0.88:
                new_level = "advanced"
            elif avg_score >= 0.75:
                new_level = "intermediate"

            if user.get('level') != new_level:
                db['users'].update_one({"email": user['email']}, {"$set": {"level": new_level}})

        # Update recommended path using metrics helper
        try:
            path = update_user_learning_path(user['email'])
        except Exception:
            traceback.print_exc()

        # Return saved result (include evaluation so frontend shows data immediately)
        # Re-fetch the saved doc to include _id
        saved = db['exercise_results'].find_one({'_id': insert_res.inserted_id})
        return saved

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Submission failed: {str(e)}")
