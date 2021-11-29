$(document).ready(function() {

    //nahodim kartinku
    //Version from 09/05 added Zoom *1
    var image = $('#image');
  
  
  
    //-----------BUTTON LOGIC------------
    $('.btnViewer').click(function(e) {
      var box = $(this).parent();
      var tool = $(box).find('.tool');
      // Esli estj tool, to otkrivajet ili zakrivajet ego
      if (tool) {
        var isOpen = tool.css('display');
        if (isOpen == 'block') {
          $(tool).hide();
          return;
        } else $(tool).show();
      }
      //esli klikajesh za ramki box, to tool propadaet
      $(document).mouseup(function(a)
      {
        if (!box.is(a.target) && box.has(a.target).length === 0){
            tool.css('display','none');
            return;
        }
      });
    });
  
  
  
  
    var click = 0;
    var i = 0;
    var arrayOfGroups = [];
    var x1,x2,y1,y2;
    var deleteClick = 0;
    var Px = 0.01;  //Pixel spacing in X
    var Py = 0.01;  //Pixel spacing in Y
    var container = $('#container');
    var width = $('#container').width();
    var height = $('#container').height();
  
  
  
    //--------------------LOADING IMAGES-------------------------
    function loadImages(sources, callback) {
      var images = {};
      var loadedImages = 0;
      var numImages = 0;
      for (var src in sources) {
        numImages++;
      }
      for (var src in sources) {
        images[src] = new Image();
        images[src].onload = function () {
          if (++loadedImages >= numImages) {
            callback(images);
          }
        };
        images[src].src = sources[src];
      }
    }
  
  //--------------------BUILD CANVAS AND DRAW---------------------------- MACCARONI CODE
    var stage;
    function buildStage(images) {
      stage = new Konva.Stage({
        container: 'container',
        width: width,
        height: height,
        draggable: false,
      });
      console.log(width,height)
      var layer = new Konva.Layer();
      var layer2 = new Konva.Layer();
      var layer3 = new Konva.Layer();
      var bigGroup = new Konva.Group({
        draggable: true,
      });
  
  
      var xray = new Konva.Image({
        image: images.xray,
      });
  
  
      console.log(images.xray.naturalHeight);
      var y = images.xray.naturalHeight;
      var x = images.xray.naturalWidth;
      var diag = Math.sqrt(x*x + y*y);
  
      //container.height = '1000px';
      //container.width = '1000px';
      xray.offsetX(x/2);
      xray.offsetY(y/2);
  
      //console.log(xray.x)
      //xray.x(diag/2 +10);
      //xray.y(diag/2 +10);
  
      xray.x(stage.width()/2);
      xray.y(stage.height()/2);
  
      xray.cache();
      xray.filters([Konva.Filters.Contrast,Konva.Filters.Brighten]);
      layer.add(xray);
      stage.add(layer);
      stage.add(layer2);
      stage.add(layer3);
  
  
      //-------------------BRIGHTNESS------------------------------
      var sliderBrightness = document.getElementById('brightnessControll');
      sliderBrightness.oninput = function () {
        xray.brightness(sliderBrightness.value);
        layer.batchDraw();
      };
  
      //------------------------CONTRAST--------------------------------------
      var contrastControll = document.getElementById('contrastControll');
      contrastControll.oninput = function () {
        xray.contrast(parseFloat(contrastControll.value));
        layer.batchDraw();
      };
  
      //---------------------ROTATE----------------------------------
      var rotationControll = document.getElementById('rotationControll');
      rotationControll.oninput = function () {
        xray.rotation(rotationControll.value);
        layer.batchDraw();
      };
  
  
      //---------------------SCALE-------------------------------------
      var oldX;
      var oldY;
      var lastPointX;
      var lastPointY;
      var scaleControll = document.getElementById('scaleControll');
      scaleControll.oninput = function () {
  
        for (let i = 0; i < arrayOfGroups.length; i++) {
          for (let j = 0; j < arrayOfGroups[i].children.length; j++) {
  
            switch (arrayOfGroups[i].children[j].getClassName()) {
              case 'Circle':
                oldX = arrayOfGroups[i].attrs.oldCoord[j][0];
                oldY = arrayOfGroups[i].attrs.oldCoord[j][1];
                arrayOfGroups[i].children[j].setAttrs({
                  x:scaleBy([oldX,oldY,0,0],scaleControll.value)[0],
                  y:scaleBy([oldX,oldY,0,0],scaleControll.value)[1]
                })
                lastPointX =  arrayOfGroups[i].children[j].getAttr('x');
                lastPointY =  arrayOfGroups[i].children[j].getAttr('y');
  
                break;
  
              case 'Line':
                var pointsArray = arrayOfGroups[i].attrs.oldCoord[j];
                arrayOfGroups[i].children[j].setAttr('points',scaleBy(pointsArray,scaleControll.value));
                break;
  
              case 'Label':
                arrayOfGroups[i].children[j].setAttrs({
                  x: lastPointX+2,
                  y: lastPointY+2
                });
                break;
            }
          }
  
        }
  
        xray.scale({ x: parseFloat(scaleControll.value), y: parseFloat(scaleControll.value) });
  
        layer.batchDraw();
        layer2.batchDraw();
  
      };
  
  
  
  
  
  
  
  
      layer2.add(new Konva.Circle({
        x:width,
        y:height,
        radius:5,
        fill:'yellow'
      }));
  
      layer2.add(new Konva.Circle({
        x:stage.width(),
        y:0,
        radius:5,
        fill:'white'
      }));
  
      layer2.add(new Konva.Circle({
        x:0,
        y:0,
        radius:5,
        fill:'white'
      }));
  
      layer2.add(new Konva.Circle({
        x:0,
        y:stage.height(),
        radius:5,
        fill:'white'
      }));
  
      layer2.add(new Konva.Circle({
        x:stage.width(),
        y:stage.height(),
        radius:5,
        fill:'white'
      }));
  
      layer2.add(new Konva.Circle({
        x:stage.width()/2,
        y:stage.height()/2,
        radius:5,
        fill:'white'
      }));
      layer2.batchDraw();
      stage.on('mousemove', function(){
  
       // console.log(getRelativePointerPosition(stage));
      })
  
      //-----------------------TEXT----------------------
  
  
      // since this text is inside of a defined area, we can center it using
      // align: 'center'
      var complexText = new Konva.Text({
        x: 10,
        y: 10,
        text:
          "Jānis Berziņš, 102093-12122, 2021/06-03\n\nSērija:CT, ART 1.25mm\n\nAttēls: 1 / 377\n\nPalielinājums:1.17\n\nW:255 C:127",
        fontSize: 15,
        fontFamily: 'Calibri',
        fill: '#fff',
        padding: 0,
        align: 'left',
      });
  
      layer3.add(complexText);
      stage.add(layer3);
  
      //-----------------------SCALE BY CONSTANT----------------------
  
      function scaleBy([p1x,p1y,p2x,p2y],scaleFactor){
        p1 = {x: p1x, y: p1y};
        p2 = {x: p2x, y: p2y};
  
        v1 = {vx: p1.x - width / 2, vy: p1.y - height / 2};
        v2 = {vx: p2.x - width / 2, vy: p2.y - height / 2};
  
        v1.vx *= scaleFactor; v1.vy *= scaleFactor;
  
        v2.vx *= scaleFactor; v2.vy *= scaleFactor;
        return [v1.vx + width / 2, v1.vy + height / 2, v2.vx + width / 2, v2.vy + height / 2]
      }
  
      //---------------------MAKE DRAGGABLE-------------------------------------
      $('#btnMove').click(function() {
        if (!$(this).hasClass('activeBtn')) {
          $(this).addClass('activeBtn');
        } else {
          $(this).removeClass('activeBtn');
        }
        layer.draggable(!layer.draggable());
      });
  
      layer.on('dragmove', function() {
        var pos = layer.position();
        layer2.position({
          x: pos.x,
          y: pos.y,
        });
        console.log('imhere');
        stage.batchDraw();
        stage.draw()
      });
  
  
      //----------------------RULER---------------------------
  
          $('#btnRuler').click(function() {
            if (!$(this).hasClass('activeBtn')) {
              $(this).addClass('activeBtn');
              if ($('#btnAngle').hasClass('activeBtn')) {
                $('#btnAngle').removeClass('activeBtn');
              }
            } else {
              $(this).removeClass('activeBtn');
            }
          });
  
          stage.on('click', function () {
            if ($('#btnRuler').hasClass('activeBtn')) {
              var pos = getRelativePointerPosition(layer);
              click++;
              if (click == 1) { // =====CLICK ONE=======
                arrayOfGroups.push(i);
                arrayOfGroups[i] = new Konva.Group({
                  draggable: true,
                  oldCoord:[]
                });
  
                createCircle(pos);
  
                x1 = pos.x;
                y1 = pos.y;
              }
  
              if (click == 2) { // ======CLICK TWO=======
  
                createCircle(pos);
  
                x2 = pos.x;
                y2 = pos.y;
  
                generateLine(x1, x2, y1, y2, i);
                click = 0;
  
                dx = Math.abs(x2 - x1);
                dy = Math.abs(y2 - y1);
  
               var L_mm = Math.sqrt( (dx * pixel_spacing_x)**2 + (dy * pixel_spacing_y)**2);
               console.log($('#scaleControll').val());
               L_mm = L_mm / $('#scaleControll').val();
  
               text = new Konva.Text({
                 text: L_mm.toFixed(3) + 'mm'
                });
  
                var label = new Konva.Label({
                  //x: (x2<x1)? x2-text.width()-2:x2+2,
                  x:x2+2,
                  y: y2+2,
                  opacity:0.9
                });
  
                label.add(
                  new Konva.Tag({
                    fill: 'yellow',
                  })
                );
  
                label.add(text);
  
                arrayOfGroups[i].add(label);
                arrayOfGroups[i].attrs.oldCoord.push([label.x(),label.y()]);
                layer2.add(arrayOfGroups[i]);
                layer2.batchDraw();
                i++;
                console.log(arrayOfGroups)
  
  
  
              }
            }
          });
  
      //-------------------------------POINTER COORDINATES-------------------
      function getRelativePointerPosition(node) {
        var transform = node.getAbsoluteTransform().copy();
        transform.invert();
        var pos = node.getStage().getPointerPosition();
        console.log(pos)
        return transform.point(pos);
      }
  
  
  
      //-------------------CREATE LINE----------------------
  
      function generateLine(x1,x2,y1,y2,i){
        var line = new Konva.Line({
          points: [x1, y1, x2, y2],
          strokeWidth: 3,
          stroke: 'red',
          class: i,
        });
        arrayOfGroups[i].add(line);
        arrayOfGroups[i].attrs.oldCoord.push([x1,y1,x2,y2]);
        layer2.add(arrayOfGroups[i]);
  
      }
  
      //-------------------CREATE CIRCLE----------------------
  
      function createCircle(pos) {
        var shape = new Konva.Circle({
          x: pos.x,
          y: pos.y,
          fill: 'red',
          radius: 4,
          class: i,
        });
        arrayOfGroups[i].add(shape);
        arrayOfGroups[i].attrs.oldCoord.push([pos.x,pos.y]);
        layer2.add(arrayOfGroups[i]);
        layer2.batchDraw();
        //arrayOfGroups.push(i);
      }
  
      //-------------------FIND ANGLE----------------------
  
      function find_angle(x1Angle,x2Angle,x3Angle,y1Angle,y2Angle,y3Angle) {
          let A = {x:x1Angle, y:y1Angle}, B = {x:x2Angle, y:y2Angle}, C = {x:x3Angle, y:y3Angle}
          var AB = Math.sqrt(Math.pow(B.x-A.x,2)+ Math.pow(B.y-A.y,2));
          var BC = Math.sqrt(Math.pow(B.x-C.x,2)+ Math.pow(B.y-C.y,2));
          var AC = Math.sqrt(Math.pow(C.x-A.x,2)+ Math.pow(C.y-A.y,2));
          var angle = ((Math.acos((BC*BC+AB*AB-AC*AC)/(2*BC*AB))) * 57.2958).toFixed(2);
  
          var complexText = new Konva.Text({
            x: x3Angle + 10,
            y: y3Angle + 10,
            text: angle + '°',
            fontSize: 20,
            fontFamily: 'Calibri',
            fill: 'black',
          });
  
          var labelAngle = new Konva.Label({
            x: x3Angle+20,
            y: y3Angle,
            opacity:0.9
          });
  
          labelAngle.add(
            new Konva.Tag({
              fill: 'red',
            })
          );
  
          labelAngle.add(complexText);
  
          arrayOfGroups[i].add(labelAngle);
          arrayOfGroups[i].attrs.oldCoord.push([labelAngle.x(),labelAngle.y()]);
          layer2.add(arrayOfGroups[i]);
          layer2.batchDraw();
          //arrayOfGroups.push(i);
  
      }
  
      //-------------------CREATE ANGLE----------------------
      var x1Angle, y1Angle, x2Angle, y2Angle, x3Angle, y3Angle;
      var clicksAngle = 0;
  
      $('#btnAngle').click(function() {
        if (!$(this).hasClass('activeBtn')) {
          if ($('#btnRuler').hasClass('activeBtn')) {
            $('#btnRuler').removeClass('activeBtn');
          }
          $(this).addClass('activeBtn');
        } else {
          $(this).removeClass('activeBtn');
        }
      });
  
      stage.on('click', function () {
        if ($('#btnAngle').hasClass('activeBtn')) {
          var pos = getRelativePointerPosition(layer);
          clicksAngle++;
          if (clicksAngle == 1) {
          // arrayOfGroups.push(i);
            arrayOfGroups[i] = new Konva.Group({
              draggable: true,
              oldCoord:[]
            });
            createCircle(pos);
            x1Angle = pos.x;
            y1Angle = pos.y;
            console.log(x1Angle,y1Angle);
          }
          if (clicksAngle == 2) {
            createCircle(pos);
            x2Angle = pos.x;
            y2Angle = pos.y;
            console.log(x2Angle,y2Angle);
            generateLine(x1Angle, x2Angle, y1Angle, y2Angle, i);
          }
          if (clicksAngle == 3) {
            createCircle(pos);
            x3Angle = pos.x;
            y3Angle = pos.y;
            console.log(x3Angle,y3Angle);
            generateLine(x2Angle, x3Angle, y2Angle, y3Angle, i);
            find_angle(x1Angle,x2Angle,x3Angle,y1Angle,y2Angle,y3Angle);
            i++;
            clicksAngle = 0;
          }
        }
      });
    }

  
    loadImages(sources, buildStage);
  
  
  });