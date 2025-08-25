// frontend/js/app.js

document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = 'http://localhost:8000/api'; // Adjust the API URL as needed

    // Function to fetch students
    async function fetchStudents() {
        try {
            const response = await fetch(`${apiUrl}/students`);
            const students = await response.json();
            displayStudents(students);
        } catch (error) {
            console.error('Error fetching students:', error);
        }
    }

    // Function to display students in the UI
    function displayStudents(students) {
        const studentList = document.getElementById('student-list');
        studentList.innerHTML = '';
        students.forEach(student => {
            const studentItem = document.createElement('div');
            studentItem.className = 'student-item';
            studentItem.innerHTML = `
                <h3>${student.name}</h3>
                <p>${student.email}</p>
                <button onclick="deleteStudent(${student.id})">Delete</button>
            `;
            studentList.appendChild(studentItem);
        });
    }

    // Function to add a new student
    async function addStudent(student) {
        try {
            const response = await fetch(`${apiUrl}/students`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(student),
            });
            if (response.ok) {
                fetchStudents();
            } else {
                console.error('Error adding student:', response.statusText);
            }
        } catch (error) {
            console.error('Error adding student:', error);
        }
    }

    // Function to delete a student
    async function deleteStudent(id) {
        try {
            const response = await fetch(`${apiUrl}/students/${id}`, {
                method: 'DELETE',
            });
            if (response.ok) {
                fetchStudents();
            } else {
                console.error('Error deleting student:', response.statusText);
            }
        } catch (error) {
            console.error('Error deleting student:', error);
        }
    }

    // Event listener for the add student form
    document.getElementById('add-student-form').addEventListener('submit', (event) => {
        event.preventDefault();
        const student = {
            name: event.target.name.value,
            email: event.target.email.value,
        };
        addStudent(student);
        event.target.reset();
    });

    // Initial fetch of students
    fetchStudents();
});