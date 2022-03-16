function refreshProjects() {
    const headers = {
        'X-TOKEN': sessionStorage.getItem('userToken')
    };
    axios.post('http://192.168.221.62:80/projects', {}, { headers: headers })
        .then(function (response) {
            console.log(response.data.data);

            const table = document.getElementById('projectsList');
            table.innerHTML = '';
            for(let project of response.data.data.projects) {
                const row = `<tr><td class="tal">${project.name}</td><td class="tal">${project.company.name}</td><td class="tar">${project.created}</td></tr>`;
                table.innerHTML += row;
            }
        })
        .catch(function (error) {
            console.error(error);
        });
}

function refreshDashboard() {
    refreshProjects();
}