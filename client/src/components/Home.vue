<template>
  <div class="container">
    <div class="row">
      <h4><a class="title" href="/">Unknown Pleasures Effect</a></h4>
    </div>
    <form method="post" action="/send" enctype="multipart/form-data" @submit.prevent="onSubmit" id="img_form">
      <div class="row">
        <div class="col s12">
          <div class="file-field">
            <div class="btn">
              <span>File</span>
              <input type="file" id="img_file" name="img_file" accept="img_file" @change="onFileChanged">
            </div>
            <div class="file-path-wrapper">
              <input class="file-path validate" type="text" placeholder="Upload Image">
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col s12">
          <button class="btn waves-effect waves-light" type="submit" name="action">Submit
            <i class="material-icons right">send</i>
          </button>
        </div>
      </div>
    </form>
    <div class="row">
      <div class="col s12 m12 l6">
        <p class="img" :class="{active: visible}">
          <img width="100%" v-bind:src="`${uploadsPath}${uploadsName}`"/>
        </p>
      </div>
      <div class="col s12 m12 l6">
        <p class="img" :class="{active: visible}">
          <img width="100%" v-bind:src="`${savePath}${saveName}`"/>
        </p>
      </div>
    </div>
    <div class="row">
      <div class="col s12">
        <a class="img__name" v-bind:href="`${savePath}${saveName}`" target="_blank">{{ saveName }}</a>
        <p v-html="error"></p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
$title-color: #2c3e50;
.title {
  color: $title-color;
  transition: .3s all;
  &:hover {
    color: lighten($title-color, 20%);
  }
}
.img {
  display: none;
}
.active {
  display: block;
}
.img__name {
  word-wrap: break-word;
}
</style>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      uploadsPath: '',
      savePath: '',
      uploadsName: '',
      saveName: '',
      visible: false,
      error: ''
    }
  },
  methods: {
    onFileChanged (event) {
      this.selectedFile = event.target.files[0]
    },
    onSubmit: function () {
      const path = 'http://localhost:8080/send'
      const form = document.querySelector('form')
      const formData = new FormData(form)
      const imageFile = document.querySelector('#img_file')
      formData.append('img_file', imageFile.files[0])
      const config = {
        headers: {
          'content-type': 'multipart/form-data'
        }
      }
      const formDataName = formData.get('img_file').name
      axios.post(path, formData, config, {
        onUploadProgress: progressEvent => {
          let percentCompleted = Math.floor((progressEvent.loaded * 100) / progressEvent.total)
          // let percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          console.log(percentCompleted)
          // fn(percentCompleted);
        }
      })
        .then(response => {
          console.log(response)
          console.log(response.data)
          this.error = ''
          if (response.data !== 'File extension not allowed') {
            this.savePath = window.location.protocol + '//' + window.location.host + '/static/image/save/'
            this.uploadsPath = window.location.protocol + '//' + window.location.host + '/static/image/uploads/'
            this.uploadsName = formDataName
            this.saveName = response.data
          } else {
            this.error = 'File extension not allowed'
          }
          if (this.uploadsName !== '') {
            this.visible = true
          }
        })
        .catch(error => {
          console.log(error)
          console.log(error.data)
          this.uploadsPath = ''
          this.savePath = ''
          this.name = ''
          this.visible = false
          this.error = 'uploaded image file size should be less than 3MB'
        })
    }
  }
}
</script>
