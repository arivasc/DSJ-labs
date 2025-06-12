using UnityEngine;

public class PlayerScript : MonoBehaviour
{
    public float Speed = 5f;

    void Start()
    {
        
    }

    void Update()
    {
        print("PlayerScript Update called");
        if (Input.GetKey(KeyCode.LeftArrow))
        {
            print("Left Arrow Pressed");
            transform.position += Vector3.left * Speed * Time.deltaTime;
        }
        if (Input.GetKey(KeyCode.RightArrow))
        {
            transform.position += Vector3.right * Speed * Time.deltaTime;
        }
        if (Input.GetKey(KeyCode.UpArrow))
        {
            transform.position += Vector3.up * Speed * Time.deltaTime;
        }
        if (Input.GetKey(KeyCode.DownArrow))
        {
            transform.position += Vector3.down * Speed * Time.deltaTime;
        }
    }
}
