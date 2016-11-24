function PlaybackManager(statusChangedListener, totalFrames, images, fps, images_url) {
    this.currentFrame = 0
    this.statusChangedListener = statusChangedListener
    this.totalFrames = totalFrames
    this.images = images
    this.duration = 1000 / fps
    this.fps = fps
    this.playback_speeds = [0.25, 0.5, 1, 1.25, 1.5, 2, 3, 5]
    this.playback_speed_index = 2
    this.running = false
    this.source = images_url
}

PlaybackManager.prototype.run = function() {
    if (!this.running) {
        return;
    }

    if (this.nextFrame != null) {
        this.currentFrame = this.nextFrame
    }

    this.loadImage(this.currentFrame, true)

    setTimeout(this.run.bind(this), this.duration); // Chang

}

PlaybackManager.prototype.initialImageLoad = function() {
    image_source = this.source + this.images[this.currentFrame]

    image = new Image()
    image.src = image_source
    image.className = "playback_image_class"

    image.style.display = "block"
    image.onload = function() {
        var playback_holder = document.getElementById("playback_holder");

        while (playback_holder.firstChild) {
            playback_holder.removeChild(playback_holder.firstChild);
        }

        for (i = 0; i < playback_holder.childNodes.length; i += 1) {
            playback_holder.childNodes[i].style.display = "none"
        }

        playback_holder.appendChild(image)
    }
}

PlaybackManager.prototype.cacheImages = function(){
    image_source = this.source + this.images[this.currentFrame]

    if ($("#preloadpit").size() == 0)
    {
        $("<div id='preloadpit'></div>").appendTo("body").hide();
    }

    image = new Image()
    var self = this
    image.onload = function() {

        $("<img src='" + image_source + "'>").appendTo("#preloadpit");


        self.statusChangedListener.onCacheUpdate(self.currentFrame,self.totalFrames)
        self.currentFrame = (self.currentFrame + 1) % self.totalFrames
        if (self.currentFrame != 0){
            self.cacheImages()
        }
    }
    image.src = image_source

}

PlaybackManager.prototype.loadImage = function(index, reactive) {
    image_source = this.source + this.images[this.currentFrame]

    image = new Image()
    image.src = image_source
    image.className = "playback_image_class"

    image.style.display = "block"
    var self = this
    image.onload = function() {
        var playback_holder = document.getElementById("playback_holder");

        for (i = 0; i < playback_holder.childNodes.length; i += 1) {
            playback_holder.childNodes[i].style.display = "none"
        }

        playback_holder.appendChild(image)

        if (self.statusChangedListener) {
            self.statusChangedListener.onFrame(self.currentFrame, self.running)
        }

        if (reactive) {
            self.nextFrame = (self.currentFrame + 1) % self.totalFrames
            if (self.nextFrame == 0) {
                self.running = false
                if (self.statusChangedListener) {
                    self.statusChangedListener.onDone()
                }
            }
        }
    }
}

PlaybackManager.prototype.getCurrentFrame = function() {
    return this.currentFrame
}

PlaybackManager.prototype.play = function() {
    if (this.running) {
        this.running = false
    } else {
        this.running = true
        this.run()
    }
    return this.running
}

PlaybackManager.prototype.forward = function() {
    forward_frames_count = this.fps * 3
    this.currentFrame = Math.min(this.currentFrame += forward_frames_count, this.totalFrames - 1)
    this.running = false
    if (this.statusChangedListener) {
        this.statusChangedListener.onDone()
    }
    this.nextFrame = null
    this.loadImage(this.currentFrame, false)
}

PlaybackManager.prototype.rewind = function() {
    rewind_frames_count = this.fps * 3
    this.currentFrame = Math.max(this.currentFrame -= rewind_frames_count, 0)
    this.running = false
    if (this.statusChangedListener) {
        this.statusChangedListener.onDone()
    }
    this.nextFrame = null
    this.loadImage(this.currentFrame, false)
}

PlaybackManager.prototype.gotoFrame = function(index) {
    this.currentFrame = index;
    this.running = false;
    if (this.statusChangedListener) {
        this.statusChangedListener.onDone()
    }
    this.nextFrame = null
    this.loadImage(this.currentFrame, false)
}


PlaybackManager.prototype.increaseSpeed = function() {
    this.playback_speed_index = Math.min(this.playback_speed_index + 1, this.playback_speeds
        .length - 1)
    playback_speed = this.playback_speeds[this.playback_speed_index]
    this.duration = 1000 / this.fps / playback_speed
    return playback_speed
}

PlaybackManager.prototype.decreaseSpeed = function() {
    this.playback_speed_index = Math.max(this.playback_speed_index - 1, 0)
    playback_speed = this.playback_speeds[this.playback_speed_index]
    this.duration = 1000 / this.fps / playback_speed
    return playback_speed
};
