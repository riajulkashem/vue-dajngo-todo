<template>
    <div class="home container">
        <h1 class="title text-center mt-5">Vuengo Todo @RK</h1>
        <hr>
        <div class="row mt-5">
            <div class="col-md-6 offset-3">
                <form class="form-inline" v-on:submit.prevent="addTask">
                    <div class="form-group">
                        <input placeholder="Task Description"
                               type="text" id="id_description"
                               class="form-control mr-3"
                               v-model="description"
                        >
                    </div>
                    <div class="form-group">
                        <select class="form-control mr-3" v-model="status">
                            <option value="">Select Status</option>
                            <option value="todo">TODO</option>
                            <option value="done">DONE</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <button class="btn btn-primary form-control" type="submit">Submit</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="row mt-5">
            <div class="col-md-6">
                <div class="todo">
                    <div class="card">
                        <div class="card-header bg-warning">
                            <h2 class=" text-light">ToDo Task List</h2>
                        </div>
                        <div class="card-body">
                            <ul class="list-group" v-for="todo in todo_list" v-bind:key="todo.id">
                                <li class="list-group-item d-flex mt-1 justify-content-between align-items-center">
                                    {{ todo.description }}
                                    <span class="btn btn-success"
                                          v-on:click="updateTask(todo.id, 'done')">Done</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="todo">
                    <div class="card">
                        <div class="card-header bg-success">
                            <h2 class="text-light">Done Task List</h2>
                        </div>
                        <div class="card-body">
                            <ul class="list-group" v-for="todo in todos_done" v-bind:key="todo.id">
                                <li class="list-group-item d-flex mt-1 justify-content-between align-items-center">
                                    {{ todo.description }}
                                    <span class="btn btn-warning" v-on:click="updateTask(todo.id, 'todo')">undo</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const API_URL = 'http://127.0.0.1:8000/'
    const AUTH_CREDENTIAL = {
        username: 'riajul',
        password: 'riajul'
    }
    import axios from 'axios'

    export default {
        name: 'Home',
        data() {
            return {
                tasks: [],
                todo_list: [],
                todos_done: [],
                description: '',
                status: '',

            }
        },
        mounted() {
            this.initTaskList()
            console.log(this.todo_list)
            console.log(this.todos_done)
        },
        methods: {
            initTaskList(taskList = null) {
                if (taskList) {
                    console.log('Im in Task List None')
                    this.todo_list = taskList.filter(task => task.status === 'todo')
                    this.todos_done = taskList.filter(task => task.status === 'done')
                } else this.getTasks()
            },
            getTasks() {
                axios({
                    method: 'get',
                    url: API_URL + 'task/',
                    auth: AUTH_CREDENTIAL
                }).then((response) => {
                    this.tasks = response.data
                    console.log(response.data)
                    console.log(this.tasks)
                    this.todo_list = this.tasks.filter(task => task.status === 'todo')
                    this.todos_done = this.tasks.filter(task => task.status === 'done')
                })
            },
            addTask() {
                if (this.description === '') {
                    alert('Please Type Todo Description')
                } else if (this.status === '') {
                    alert('Please Select TODO Status')
                } else {
                    axios({
                        method: 'post',
                        url: API_URL + 'task/',
                        data: {
                            description: this.description,
                            status: this.status
                        },
                        auth: AUTH_CREDENTIAL
                    }).then((response) => {
                        let newTask = {
                            'id': response.data.id,
                            'description': this.description,
                            'status': this.status
                        }
                        this.tasks.push(newTask)
                        this.description = ''
                        this.status = 'todo'
                        this.initTaskList(this.tasks)
                        $('form')[0].reset()
                    }).catch((error) => {
                        console.log(error)
                    })
                }
            },
            updateTask(task_id, status) {
                const task = this.tasks.filter(task => task.id === task_id)[0]
                console.log(status)
                axios({
                    method: 'put',
                    url: API_URL + 'task/' + task_id + '/',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    data: {
                        status: status,
                        description: task.description
                    },
                    auth: AUTH_CREDENTIAL
                }).then(() => {
                    task.status = status
                    this.initTaskList(this.tasks)
                })
            }
        }
    }
</script>

<style lang="scss">

</style>
