# src/exercises_data.py

EXERCISES = {
    "squat_high_bar_leg": {
        "name": "Squat High Bar (Leg)",
        "trainer_video": "squat_trainer.mp4",  # файл эталонного видео, положим в data/trainers
        "angles": {
            "shoulder-elbow-wrist-left": {
                "ideal_min": 150,
                "ideal_max": 180,
                "description": (
                    "Угол между плечом, локтем и запястьем, когда держим штангу. "
                    "Руки должны быть в комфортном положении, локти не 'падают' вниз."
                )
            },
            "hip-knee-ankle-left": {
                "ideal_min": 80,
                "ideal_max": 100,
                "description": (
                    "Угол в нижней точке приседа. Следим за глубиной, "
                    "чтобы колени не выходили слишком далеко за носки."
                )
            }
        },
        "notes": (
            "Спина ровная, взгляд вперёд, колени направлены в сторону носков. "
            "Держим корпус напряжённым, не допускаем прогиба в пояснице."
        )
    }
}
