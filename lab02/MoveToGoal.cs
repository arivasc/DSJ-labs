using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class MoveToGoal : MonoBehaviour {

    public float speed = 2.0f;
    public Transform goal;

    void Start() {
        
    }

    void LateUpdate() {
        Vector3 direction = goal.position - this.transform.position;
        this.transform.Translate(direction.normalized * speed * Time.deltaTime);

    }
}
