function handleFiles(files) {
      var d = document.getElementById("target_div");

      if (!files.length) {
        d.innerHTML = "<p>No files selected!</p>";
      } else {
        for (var i=0; i < files.length; i++) {

          var img = document.createElement("img");
          img.src = window.URL.createObjectURL(files[i]);;
          img.height = 350;
          img.width = 350;
          img.onload = function() {
            window.URL.revokeObjectURL(this.src);
          }
          d.appendChild(img);

//          var info = document.createElement("li")
//          info.innerHTML = files[i].name + ": " + files[i].size + " bytes"
//          info.innerHTML = files[i].name
//          d.appendChild(info)
        }
      }
    }