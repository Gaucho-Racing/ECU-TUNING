            QSlider::groove:horizontal {
                border: 1px solid #ccc;
                background: purple;  /* Set the groove background color to purple */
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: qradialgradient(
                    cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,
                    radius: 1.35, stop: 0 #fff, stop: 1 #777
                );
                width: 15px;
                margin-top: -2px;
                margin-bottom: -2px;
                border-radius: 7px;
            }
        """)