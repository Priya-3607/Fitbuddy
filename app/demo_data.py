from .schemas import WorkoutPlan, WorkoutDay, Exercise

def demo_workout_plan(
    goal: str,
    intensity: str,
    workout_schedule: str = "5 days/week",
    experience_level: str = "beginner"
) -> WorkoutPlan:
    # Determine workout vs rest days based on schedule
    sched_lower = (workout_schedule or "").lower()
    if "3 day" in sched_lower:
        active_days_indices = {0, 2, 4}  # Days 1, 3, 5
        training_count = 3
    elif "4 day" in sched_lower:
        active_days_indices = {0, 1, 3, 4}  # Days 1, 2, 4, 5
        training_count = 4
    elif "6 day" in sched_lower:
        active_days_indices = {0, 1, 2, 3, 4, 5}  # Days 1-6
        training_count = 6
    elif "7 day" in sched_lower:
        active_days_indices = {0, 1, 2, 3, 4, 5, 6}  # All days
        training_count = 7
    else:
        # Default to 5 days/week (Days 1, 2, 3, 5, 6)
        active_days_indices = {0, 1, 2, 4, 5}
        training_count = 5

    goal_clean = (goal or "general wellness").lower()
    intensity_clean = (intensity or "medium").capitalize()
    exp_clean = (experience_level or "beginner").capitalize()

    base = {
        "title": f"FitBuddy 7-Day {goal_clean.title()} Plan ({training_count} Workout Days)",
        "summary": f"A {intensity_clean}-intensity {exp_clean} plan tailored for {goal_clean} with {training_count} active training days.",
        "safety_note": "This plan is for general wellness. Stop immediately if you experience pain, dizziness, chest pain, or unusual shortness of breath.",
        "days": []
    }

    # Goal-specific exercise pools for training days
    if "muscle" in goal_clean or "gain" in goal_clean:
        day_templates = [
            ("Upper Body Hypertrophy", [
                Exercise(name="Dumbbell Bench Press", sets="3", reps_or_duration="8–12", rest="60–90 sec", notes="Focus on full range of motion."),
                Exercise(name="Bent-over Dumbbell Row", sets="3", reps_or_duration="8–12", rest="60–90 sec", notes="Keep core tight and spine neutral."),
                Exercise(name="Standing Dumbbell Shoulder Press", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Control the descent."),
                Exercise(name="Bicep Dumbbell Curls", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Avoid using momentum.")
            ]),
            ("Lower Body Hypertrophy", [
                Exercise(name="Dumbbell Goblet Squats", sets="3–4", reps_or_duration="8–12", rest="90 sec", notes="Keep chest up and knees tracking over toes."),
                Exercise(name="Romanian Deadlifts", sets="3", reps_or_duration="10–12", rest="90 sec", notes="Hinge at hips, slight knee bend."),
                Exercise(name="Walking Lunges", sets="3", reps_or_duration="10 per leg", rest="60 sec", notes="Keep torso upright."),
                Exercise(name="Glute Bridges", sets="3", reps_or_duration="12–15", rest="60 sec", notes="Squeeze glutes at top pause.")
            ]),
            ("Full Body Power", [
                Exercise(name="Incline Push-ups", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Modify angle as needed."),
                Exercise(name="Lat Pulldowns or Band Pulls", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Squeeze shoulder blades together."),
                Exercise(name="Bulgarian Split Squats", sets="3", reps_or_duration="8–10 per leg", rest="90 sec", notes="Drive through front heel."),
                Exercise(name="Plank Hold", sets="3", reps_or_duration="30–45 sec", rest="45 sec", notes="Engage core and glutes.")
            ]),
            ("Push / Upper Focus", [
                Exercise(name="Dumbbell Chest Flyes", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Maintain slight elbow bend."),
                Exercise(name="Lateral Dumbbell Raises", sets="3", reps_or_duration="12–15", rest="45 sec", notes="Control the movement."),
                Exercise(name="Tricep Overhead Extension", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Keep elbows close to head."),
            ]),
            ("Pull / Lower Focus", [
                Exercise(name="Dumbbell Single-arm Rows", sets="3", reps_or_duration="10–12 per side", rest="60 sec", notes="Pull towards hip."),
                Exercise(name="Bodyweight Hamstring Curls", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Slow eccentric lowering."),
                Exercise(name="Calf Raises", sets="3", reps_or_duration="15–20", rest="45 sec", notes="Full stretch at bottom, pause at top.")
            ]),
            ("Core & Conditioning", [
                Exercise(name="Russian Twists", sets="3", reps_or_duration="15 per side", rest="45 sec", notes="Engage obliques."),
                Exercise(name="Hanging or Lying Knee Raises", sets="3", reps_or_duration="10–12", rest="45 sec", notes="Avoid swinging."),
                Exercise(name="Farmer's Dumbbell Carry", sets="3", reps_or_duration="40 meters", rest="60 sec", notes="Maintain posture.")
            ]),
            ("Full Body Strength", [
                Exercise(name="Barbell / Dumbbell Squat", sets="3", reps_or_duration="8–10", rest="90 sec", notes="Solid stance."),
                Exercise(name="Push-ups", sets="3", reps_or_duration="8–12", rest="60 sec", notes="Full body alignment."),
                Exercise(name="Dumbbell Rows", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Controlled pull.")
            ])
        ]
    elif "weight" in goal_clean or "loss" in goal_clean or "fat" in goal_clean:
        day_templates = [
            ("Full Body Fat Burn Circuit", [
                Exercise(name="Bodyweight Air Squats", sets="3", reps_or_duration="15–20", rest="45 sec", notes="Keep pace brisk but controlled."),
                Exercise(name="Incline Push-ups", sets="3", reps_or_duration="12–15", rest="45 sec", notes="Maintain plank line."),
                Exercise(name="Mountain Climbers", sets="3", reps_or_duration="30 sec", rest="30 sec", notes="Keep hips low."),
                Exercise(name="Jumping Jacks / Shadow Boxing", sets="3", reps_or_duration="45 sec", rest="30 sec", notes="Light on feet.")
            ]),
            ("Cardio & Core Intervals", [
                Exercise(name="High Knees / Fast Marching", sets="4", reps_or_duration="30 sec work", rest="30 sec rest", notes="Drive arms and knees."),
                Exercise(name="Bicycle Crunches", sets="3", reps_or_duration="15 per side", rest="45 sec", notes="Elbow to opposite knee."),
                Exercise(name="Plank Shoulder Taps", sets="3", reps_or_duration="12 per side", rest="45 sec", notes="Minimize hip sway."),
                Exercise(name="Speed Skaters", sets="3", reps_or_duration="40 sec", rest="30 sec", notes="Lateral bounding.")
            ]),
            ("Lower Body & Heart Rate Boost", [
                Exercise(name="Reverse Lunges", sets="3", reps_or_duration="12 per leg", rest="45 sec", notes="Step back smoothly."),
                Exercise(name="Glute Bridge Pulses", sets="3", reps_or_duration="20 reps", rest="45 sec", notes="Squeeze at top."),
                Exercise(name="Kettlebell / Dumbbell Swings", sets="3", reps_or_duration="15 reps", rest="60 sec", notes="Hinge hips forcefully."),
                Exercise(name="Bodyweight Step-ups", sets="3", reps_or_duration="12 per leg", rest="45 sec", notes="Drive through lead leg.")
            ]),
            ("Upper Body & Cardio Conditioning", [
                Exercise(name="Dumbbell Thrusters (Squat to Press)", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Fluid motion."),
                Exercise(name="Dumbbell Renegade Rows", sets="3", reps_or_duration="8 per side", rest="60 sec", notes="Wide foot stance for stability."),
                Exercise(name="Burpees (Low Impact Option)", sets="3", reps_or_duration="8–10", rest="60 sec", notes="Step back instead of jump if needed."),
                Exercise(name="Flutter Kicks", sets="3", reps_or_duration="30 sec", rest="30 sec", notes="Lower back flat against floor.")
            ]),
            ("Metabolic Conditioning", [
                Exercise(name="Bodyweight Squat to Knee Raise", sets="3", reps_or_duration="15 reps", rest="45 sec", notes="Cross-body knee lift."),
                Exercise(name="Bear Crawl Hold", sets="3", reps_or_duration="30 sec", rest="45 sec", notes="Knees hovering 2 inches off floor."),
                Exercise(name="Jump Rope / Fast Skipping", sets="4", reps_or_duration="45 sec", rest="30 sec", notes="Stay light on balls of feet.")
            ]),
            ("Full Body Sweater", [
                Exercise(name="Sumo Squats", sets="3", reps_or_duration="15 reps", rest="45 sec", notes="Wide stance, toes flared."),
                Exercise(name="Commando Planks", sets="3", reps_or_duration="10 reps total", rest="45 sec", notes="Elbow to hand transition."),
                Exercise(name="Skaters", sets="3", reps_or_duration="30 sec", rest="30 sec", notes="Side to side agility.")
            ]),
            ("Cardio Blitz", [
                Exercise(name="Jumping Jacks", sets="4", reps_or_duration="45 sec", rest="30 sec", notes="Consistent cadence."),
                Exercise(name="Bodyweight Squats", sets="3", reps_or_duration="20 reps", rest="45 sec", notes="Full depth.")
            ])
        ]
    elif "flexibility" in goal_clean:
        day_templates = [
            ("Dynamic Mobility & Flow", [
                Exercise(name="Cat-Cow Pose", sets="2", reps_or_duration="60 sec", rest="30 sec", notes="Synchronize with breathing."),
                Exercise(name="Downward-Facing Dog", sets="3", reps_or_duration="45 sec hold", rest="30 sec", notes="Pedal feet gently."),
                Exercise(name="World's Greatest Stretch", sets="2", reps_or_duration="5 per side", rest="45 sec", notes="Step deep into lunge and rotate chest."),
                Exercise(name="Child's Pose", sets="2", reps_or_duration="60 sec hold", rest="30 sec", notes="Deep nasal breathing.")
            ]),
            ("Hip Opener & Spine Mobility", [
                Exercise(name="Pigeon Pose", sets="2", reps_or_duration="45 sec per side", rest="30 sec", notes="Breathe into tight hips."),
                Exercise(name="Seated Butterfly Stretch", sets="2", reps_or_duration="60 sec hold", rest="30 sec", notes="Gentle pressure on thighs."),
                Exercise(name="Thoracic Spine Windmills", sets="2", reps_or_duration="8 per side", rest="30 sec", notes="Lying side twist."),
                Exercise(name="Cobra Pose", sets="2", reps_or_duration="30 sec hold", rest="30 sec", notes="Extend chest up gently.")
            ]),
            ("Hamstring & Calves Lengthening", [
                Exercise(name="Seated Single-Leg Forward Fold", sets="2", reps_or_duration="45 sec per leg", rest="30 sec", notes="Hinge from hips, don't round lower back."),
                Exercise(name="Standing Calf & Achilles Stretch", sets="2", reps_or_duration="45 sec per leg", rest="30 sec", notes="Press heel into ground."),
                Exercise(name="Low Lunge Quadriceps Stretch", sets="2", reps_or_duration="45 sec per leg", rest="30 sec", notes="Tuck pelvis slightly.")
            ]),
            ("Shoulder & Upper Body Mobility", [
                Exercise(name="Doorway Chest Stretch", sets="2", reps_or_duration="45 sec", rest="30 sec", notes="Lean forward gently."),
                Exercise(name="Thread the Needle Stretch", sets="2", reps_or_duration="45 sec per side", rest="30 sec", notes="Shoulder to mat."),
                Exercise(name="Puppy Dog Pose", sets="2", reps_or_duration="60 sec hold", rest="30 sec", notes="Melt heart towards floor.")
            ]),
            ("Full Body Alignment", [
                Exercise(name="Standing Side Bends", sets="2", reps_or_duration="45 sec per side", rest="30 sec", notes="Reach arm high."),
                Exercise(name="Supine Spinal Twist", sets="2", reps_or_duration="60 sec per side", rest="30 sec", notes="Shoulders flat on mat.")
            ]),
            ("Posterior Chain Focus", [
                Exercise(name="Ragdoll Forward Fold", sets="2", reps_or_duration="60 sec hold", rest="30 sec", notes="Slight knee bend, sway hips."),
                Exercise(name="Happy Baby Pose", sets="2", reps_or_duration="60 sec hold", rest="30 sec", notes="Pull knees down toward armpits.")
            ]),
            ("Restorative Yoga Flow", [
                Exercise(name="Legs-Up-The-Wall Pose", sets="1", reps_or_duration="5 min hold", rest="None", notes="Restorative inversion.")
            ])
        ]
    elif "strength" in goal_clean:
        day_templates = [
            ("Lower Body Heavy Strength", [
                Exercise(name="Barbell / Heavy Dumbbell Squat", sets="4", reps_or_duration="5–8", rest="120 sec", notes="Focus on bracing core and depth."),
                Exercise(name="Romanian Deadlifts", sets="3", reps_or_duration="6–8", rest="90 sec", notes="Control hip hinge."),
                Exercise(name="Bulgarian Split Squats", sets="3", reps_or_duration="6–8 per leg", rest="90 sec", notes="Drive through front heel."),
                Exercise(name="Heavy Glute Bridges", sets="3", reps_or_duration="8–10", rest="90 sec", notes="Pause at top extension.")
            ]),
            ("Upper Body Push / Pull", [
                Exercise(name="Flat Dumbbell Bench Press", sets="4", reps_or_duration="6–8", rest="120 sec", notes="Keep shoulder blades retracted."),
                Exercise(name="Heavy Single-Arm Dumbbell Row", sets="4", reps_or_duration="6–8 per side", rest="90 sec", notes="Pull with back muscles."),
                Exercise(name="Overhead Press", sets="3", reps_or_duration="6–8", rest="90 sec", notes="Squeeze glutes and brace abdominal wall."),
                Exercise(name="Face Pulls / Band Pull-aparts", sets="3", reps_or_duration="12–15", rest="60 sec", notes="Upper back rear delt focus.")
            ]),
            ("Posterior Chain Strength", [
                Exercise(name="Conventional / Dumbbell Deadlift", sets="4", reps_or_duration="5 reps", rest="120 sec", notes="Maintain flat back."),
                Exercise(name="Lat Pulldowns / Pull-ups", sets="3", reps_or_duration="6–8", rest="90 sec", notes="Pull elbows down to ribs."),
                Exercise(name="Farmer's Heavy Walk", sets="3", reps_or_duration="30 sec walk", rest="90 sec", notes="Upright posture, tight grip.")
            ]),
            ("Conditioning & Core Strength", [
                Exercise(name="Incline Push-up to Plank", sets="3", reps_or_duration="8–10", rest="90 sec", notes="Strict form."),
                Exercise(name="Ab Wheel Rollouts or Walkouts", sets="3", reps_or_duration="8–10", rest="60 sec", notes="Protect lower back."),
                Exercise(name="Heavy Goblet Hold Step-ups", sets="3", reps_or_duration="8 per leg", rest="90 sec", notes="Controlled push.")
            ]),
            ("Upper Body Power", [
                Exercise(name="Incline Dumbbell Press", sets="3", reps_or_duration="6–8", rest="90 sec", notes="Solid shoulder stability."),
                Exercise(name="Chest Supported Dumbbell Rows", sets="3", reps_or_duration="8–10", rest="90 sec", notes="Squeeze back.")
            ]),
            ("Lower Body Power", [
                Exercise(name="Front Dumbbell Squats", sets="3", reps_or_duration="6–8", rest="90 sec", notes="Elbows high."),
                Exercise(name="Good Mornings / Hinge", sets="3", reps_or_duration="8–10", rest="90 sec", notes="Hinge smoothly.")
            ]),
            ("Full Body Compound", [
                Exercise(name="Squat to Press", sets="3", reps_or_duration="6–8", rest="90 sec", notes="Integrated strength.")
            ])
        ]
    else:  # General wellness / default
        day_templates = [
            ("Full Body Mobility & Light Strength", [
                Exercise(name="Bodyweight Squats", sets="3", reps_or_duration="10–12", rest="60 sec", notes="Smooth pace."),
                Exercise(name="Wall / Incline Push-ups", sets="3", reps_or_duration="8–12", rest="60 sec", notes="Comfortable range."),
                Exercise(name="Glute Bridges", sets="3", reps_or_duration="12 reps", rest="60 sec", notes="Squeeze glutes."),
                Exercise(name="Bird-Dog Hold", sets="3", reps_or_duration="8 per side", rest="45 sec", notes="Opposite arm and leg extension.")
            ]),
            ("Gentle Cardio & Core", [
                Exercise(name="Brisk Walk / Light Jog", sets="1", reps_or_duration="20–30 min", rest="As needed", notes="Maintain easy conversational pace."),
                Exercise(name="Plank Hold", sets="3", reps_or_duration="20–30 sec", rest="45 sec", notes="Focus on steady breathing."),
                Exercise(name="Standing Knee-to-Elbow", sets="3", reps_or_duration="10 per side", rest="45 sec", notes="Gentle core activation.")
            ]),
            ("Lower Body Wellness", [
                Exercise(name="Assisted Lunges", sets="3", reps_or_duration="8 per leg", rest="60 sec", notes="Hold chair/wall for balance if needed."),
                Exercise(name="Step-ups", sets="3", reps_or_duration="10 per leg", rest="60 sec", notes="Use low step."),
                Exercise(name="Calf Raises", sets="3", reps_or_duration="15 reps", rest="45 sec", notes="Smooth movement.")
            ]),
            ("Upper Body & Posture", [
                Exercise(name="Band Pull-Aparts or Doorway Rows", sets="3", reps_or_duration="12 reps", rest="45 sec", notes="Focus on upper back posture."),
                Exercise(name="Countertop Push-ups", sets="3", reps_or_duration="10 reps", rest="60 sec", notes="Keep core steady."),
                Exercise(name="Arm Circles & Shoulder Rolls", sets="2", reps_or_duration="45 sec", rest="30 sec", notes="Loosen shoulders.")
            ]),
            ("Functional Movement", [
                Exercise(name="Bodyweight Hinge / Good Morning", sets="3", reps_or_duration="10–12", rest="45 sec", notes="Hinge hips back."),
                Exercise(name="Side Plank on Knees", sets="3", reps_or_duration="20 sec per side", rest="45 sec", notes="Lateral core strength.")
            ]),
            ("Active Cardio Flow", [
                Exercise(name="Light Outdoor Walk", sets="1", reps_or_duration="25 min", rest="None", notes="Enjoy natural light and pace."),
                Exercise(name="Standing Torso Twists", sets="2", reps_or_duration="45 sec", rest="30 sec", notes="Loosen waist.")
            ]),
            ("Full Body Gentle Movement", [
                Exercise(name="Bodyweight Squat to Stretch", sets="3", reps_or_duration="10 reps", rest="45 sec", notes="Gentle dynamic stretch.")
            ])
        ]

    # Build 7 days
    training_day_ptr = 0
    for day_idx in range(7):
        day_label = f"Day {day_idx + 1}"
        if day_idx in active_days_indices:
            focus_title, exercises = day_templates[training_day_ptr % len(day_templates)]
            training_day_ptr += 1
            base["days"].append(WorkoutDay(
                day=day_label,
                focus=focus_title,
                warm_up="5–10 min dynamic mobility & light pulse raiser.",
                exercises=exercises,
                cool_down="5 min gentle static stretching & deep breathing.",
                recovery_tip="Rehydrate and consume protein-rich recovery meal."
            ))
        else:
            base["days"].append(WorkoutDay(
                day=day_label,
                focus="Active Recovery & Rest",
                warm_up="Optional 5 min light walk.",
                exercises=[
                    Exercise(name="Easy Walk or Light Cycling", sets="1", reps_or_duration="20–30 min", rest="As needed", notes="Keep intensity low; focus on movement and fresh air."),
                    Exercise(name="Full Body Gentle Stretch", sets="1", reps_or_duration="10 min", rest="As needed", notes="Focus on lower back, hamstrings, and shoulders.")
                ],
                cool_down="Hydration and relaxation.",
                recovery_tip="Prioritize 7–9 hours of quality sleep for physical recovery."
            ))

    return WorkoutPlan.model_validate(base)

