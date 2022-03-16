function setProjectsErrorText(text) {
    if (text) {
        document.getElementById('projectsMessage').innerText = `${text}`;
        document.getElementById('projectsTable').hidden = true;
    } else {
        document.getElementById('projectsMessage').innerText = ``;
        document.getElementById('projectsTable').hidden = false;
    }
}

function refreshProjects() {
    const headers = {
        'X-TOKEN': sessionStorage.getItem('userToken') || ''
    };
    axios.post('http://192.168.221.62:80/projects', {}, { headers: headers })
        .then(function (response) {
            if (response.data.success) {
                setProjectsErrorText('');
                const projects = response.data.data.projects || [];
                console.log(projects);

                const table = document.getElementById('projectsList');
                table.innerHTML = '';
                if (projects && projects.length) {
                    for (let project of projects) {
                        const row = `<tr><td class="tal">${project.name}</td><td class="tal">${project.company.name}</td><td class="tar">${project.created}</td></tr>`;
                        table.innerHTML += row;
                    }
                }
            } else {
                setProjectsErrorText(response.data.message);
            }
        })
        .catch(function (error) {
            console.error(error);
        });
}

function refreshDashboard() {
    refreshProjects();
}