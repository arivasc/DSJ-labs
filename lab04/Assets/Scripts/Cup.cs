
using UnityEngine;

public class Cup : MonoBehaviour
{
    // Contador individual por cada Cup
    public int score = 0;

    void OnTriggerEnter2D(Collider2D collision)
    {
        Debug.Log("Trigger entered with: " + collision.gameObject.name);
        // Verifica si lo que entró es una pelota
        Ball ball = collision.GetComponent<Ball>();
        if (ball != null)
        {
            score++;
            Debug.Log("Ball entered cup! Total: " + score);

            // O actualizar un contador global
            GameManager.Instance.AddScore();
        }
    }
	
}
