# src/exercises_data.py

EXERCISES = {
    "squat": {
        "name": "Приседания со штангой (High Bar)",
        "trainer_video": "squat_trainer.mp4",  # файл эталонного видео
        "angles": {
            "shoulder-elbow-wrist-left": {
                "ideal_min": 150,
                "ideal_max": 180,
                "description": "Угол между плечом, локтем и запястьем при удержании штанги."
            },
            "hip-knee-ankle-left": {
                "ideal_min": 80,
                "ideal_max": 100,
                "description": "Угол в нижней точке приседа (глубина приседа)."
            }
        },
        "notes": "Спина ровная, колени не выходят за носки, взгляд вперёд."
    }
}
