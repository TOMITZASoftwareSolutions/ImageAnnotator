 function TagManager(tags, totalFrames) {
     this.tags = tags;
     this.selected = null;
     this.tagsForImages = new Array(totalFrames)
 }

 TagManager.prototype.setSelected = function(tag) {
     for (var i = this.tags.length - 1; i >= 0; i--) {
         if (this.tags[i] == tag) {
             if (this.selected != i) {
                 this.selected = i
             } else {
                 this.selected = null
             }
         }
     }
 }

 TagManager.prototype.getSelected = function() {
     return this.selected
 };

 TagManager.prototype.tagImageAtIndex = function(index) {
     if (this.selected) {
         this.tagsForImages[index] = this.tags[this.selected]
     }else{
        this.tagsForImages[index] = 'non-class'
     }
     return this.selected
 }

 TagManager.prototype.getTagsForUmages = function() {
     return this.tagsForImages
 }

 TagManager.prototype.getTagIndexForImageAt = function(imageIndex){
    tagIndex = this.tags.map(function(e) { return e; }).indexOf(this.tagsForImages[imageIndex]);
    if (tagIndex==-1) {
        tagIndex = null
    }
    return tagIndex
 }

 TagManager.prototype.addTag = function(tagName){
    this.tags.push(tagName)
 }

 TagManager.prototype.containsTag = function(tagName){
    return this.tags.indexOf(tagName) != -1;
 }
