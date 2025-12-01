package com.cs407.lab09

import android.hardware.Sensor
import android.hardware.SensorEvent
import androidx.compose.ui.geometry.Offset
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

class BallViewModel : ViewModel() {

    private var ball: Ball? = null
    private var lastTimestamp: Long = 0L

    // Expose the ball's position as a StateFlow
    private val _ballPosition = MutableStateFlow(Offset.Zero)
    val ballPosition: StateFlow<Offset> = _ballPosition.asStateFlow()

    /**
     * Called by the UI when the game field's size is known.
     */
    fun initBall(fieldWidth: Float, fieldHeight: Float, ballSizePx: Float) {
        if (ball == null) {
            ball = Ball(fieldWidth, fieldHeight, ballSizePx)
            ball?.reset()
            _ballPosition.value = Offset(ball!!.posX, ball!!.posY)
        }
    }

    /**
     * Called by the SensorEventListener in the UI.
     */
    fun onSensorDataChanged(event: SensorEvent) {
        // Ensure ball is initialized
        val currentBall = ball ?: return

        if (event.sensor.type == Sensor.TYPE_GRAVITY) {
            if (lastTimestamp != 0L) {
                val dT = (event.timestamp - lastTimestamp) / 1_000_000_000f

                // The sensor's x and y-axis are inverted
                // Gravity sensor returns m/s^2. We need to scale it to pixels/s^2 for the ball to move visibly.
                // A factor of 100-500 is usually good for screen coordinates.
                val scalingFactor = 100f
                
                // Tilt Right (Right side down) -> values[0] < 0. Ball should move Right (+X).
                // So xAcc should be positive. xAcc = -values[0].
                val xAcc = -event.values[0] * scalingFactor
                
                // Upright (Top side up) -> values[1] > 0. Ball should move Down (+Y).
                // So yAcc should be positive. yAcc = values[1].
                val yAcc = event.values[1] * scalingFactor

                currentBall.updatePositionAndVelocity(xAcc, yAcc, dT)

                _ballPosition.update { Offset(currentBall.posX, currentBall.posY) }
            }

            lastTimestamp = event.timestamp
        }
    }

    fun reset() {
        ball?.reset()
        ball?.let {
            _ballPosition.value = Offset(it.posX, it.posY)
        }
        lastTimestamp = 0L
    }
}