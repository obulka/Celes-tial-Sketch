using UnityEngine;
 
public class StreetViewCamera : MonoBehaviour {
    public float speed = 3.5f;
    private float X;
    private float Y;
    private bool draggable = true;

    void Update() {
        if(Input.GetMouseButton(0) && draggable) {
            transform.Rotate(new Vector3(Input.GetAxis("Mouse Y") * speed, -Input.GetAxis("Mouse X") * speed, 0));
            X = Mathf.Clamp(transform.rotation.eulerAngles.x, -360, 360);
            Y = transform.rotation.eulerAngles.y;
            transform.rotation = Quaternion.Euler(X, Y, 0);
        }
    }

    public void ToggleDraggable() {
        draggable = !draggable;
    }
}