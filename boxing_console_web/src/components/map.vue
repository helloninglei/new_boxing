<template>
	<div>
		<div class="baiduTop" style="padding:10px 0;">
		  	<label >地点：</label>
		  	<input id="where" name="where" type="text" placeholder="请输入搜索的地址" v-model='address' @blur="onblur()"  @focus="onfocus()">
			<button type="button" @click="sear();">查找</button>
		  	<label style="margin-left:180px">经纬度：</label>
		  	<input id="lonlat" name="lonlat" type="text" readonly="readonly" placeholder="点击地图地点获取经纬度">
		  	<button class="mapSure">确定</button>
		 </div>
		 <div style="width:750px;height:600px;border:1px solid gray" id="container" margin-top="20px"></div>
	</div>
</template>
<style type="text/css">  
    html{height:100%}  
    body{height:100%;margin:0px;padding:0px}  
    #container{height:100%}  
</style>
<script>
	// import BMap from 'BMap';
    export default {
        data() {
            return {
                address : '',
            }
        },
        components: {

        },
        created() {
            
        },
        mounted(){
        	this.map();
        },
        methods: {
        	map(){  
		        var mapArr = {};
	            console.log($('#container'))
				//在指定的容器内创建地图实例
				var map = new BMap.Map("container");
				let $this=this;
				this.map = map ;
				map.setDefaultCursor("crosshair");//设置地图默认的鼠标指针样式
				map.enableScrollWheelZoom();//启用滚轮放大缩小，默认禁用。
				//创建点坐标
				var point = new BMap.Point(120.386266, 30.307407);
				//初始化地图，设置中心点坐标和地图级别
				map.centerAndZoom(point, 15);;
				//panTo()方法 等待两秒钟后-让地图平滑移动至新中心点
				/**window.setTimeout(function(){ 
				map.panTo(new BMap.Point(120.386266, 30.307407)); }, 2000);**/
				//***********************地址解析类  
				var gc = new BMap.Geocoder();
				//NavigationControl 地图平移缩放控件，默认位于地图左上方 它包含控制地图的平移和缩放的功能。
				map.addControl(new BMap.NavigationControl()); 
				//OverviewMapControl 缩略地图控件，默认位于地图右下方，是一个可折叠的缩略地图
				map.addControl(new BMap.OverviewMapControl());
				//ScaleControl：比例尺控件，默认位于地图左下方，显示地图的比例关系。
				map.addControl(new BMap.ScaleControl());
				//MapTypeControl：地图类型控件，默认位于地图右上方。
				map.addControl(new BMap.MapTypeControl());
				//CopyrightControl：版权控件，默认位于地图左下方
				map.addControl(new BMap.CopyrightControl());
				// 创建标注  
				var marker = new BMap.Marker(point);   
				// 将标注添加到地图中
				map.addOverlay(marker);

				//marker的enableDragging和disableDragging方法可用来开启和关闭标注的拖拽功能。
				marker.enableDragging();
				//监听标注的dragend事件来捕获拖拽后标注的最新位置
				marker.addEventListener("dragend",function(e){
					gc.getLocation(e.point, function(rs){ 
				        	showLocationInfo(e.point, rs);  
				    	});  
				});
				map.addEventListener("click", function(e){//地图单击事件
					console.log(e);
					document.getElementById("lonlat").value = e.point.lng + ", " + e.point.lat;
					mapArr.lng = e.point.lng;
					mapArr.lat = e.point.lat;
					var lng = e.point.lng;
					var lat = e.point.lat;
					// $this.addressInfo(lng,lat)
					$this.addressInfo(lng, lat,mapArr)
				});
				var myCity = new BMap.LocalCity();
					myCity.get(this.iploac);
				
				var traffic = new BMap.TrafficLayer();     
				// 将图层添加到地图上  
				map.addTileLayer(traffic); 
				$(".mapSure").on('click',function(event){
			   	var point = new BMap.Point(mapArr.lng,mapArr.lat);
			   	var geoc = new BMap.Geocoder();
				   geoc.getLocation(point, function(rs){
						var addComp = rs.addressComponents;
						var str = addComp.province  + addComp.city + addComp.district + addComp.street + addComp.streetNumber;
				   });
				  if(Object.getOwnPropertyNames(mapArr).length != 3 ||　$("#lonlat").val() == ""){
					   alert('请点击标注获取经纬度');
				   }else{
					   
					   Constans.removeItemStorage('mapInfo');
					   Constans.setItemStorage('mapInfo',mapArr);
					   event.preventDefault();
					   $('#dialog-baiduMap').dialog('close');
					   $('#dialog-match-baiduMap').dialog('close');
					   event.stopPropagation();
					   
					   var address = $("#where").val();
					   $("#proAddress").val(address);
					   console.log("0000000000000000000000000000000=====================");
					   $("#matchTakeAddress").val(address);
					   console.log("1111111111111111111111111111111=====================");
					   $("#where").val('');
				    $("#lonlat").val('');
				   }
				})  
		     },
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        alert('submit!');
                    } else {
                        console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            },
             showLocationInfo(pt, rs){  
			    var opts = {  
			      width : 250,     //信息窗口宽度  
			      height: 150,     //信息窗口高度  
			      title : "当前位置"  //信息窗口标题  
			    }  
			    
			    var addComp = rs.addressComponents;  
			    var addr = "当前位置：" + addComp.province + ", " + addComp.city + ", " + addComp.district + ", " + addComp.street + ", " + addComp.streetNumber + "<br/>";  
			    addr += "纬度: " + pt.lat + ", " + "经度：" + pt.lng;  
			    var infoWindow = new BMap.InfoWindow(addr, opts);  //创建信息窗口对象  
			    marker.openInfoWindow(infoWindow);    
			} ,
			sear(){//地图搜索
				var local = new BMap.LocalSearch(this.map, {
			  		renderOptions:{map: this.map}
				});
				local.search(this.address);
			},
			addressInfo(lng, lat,mapArr) {
				var point = new BMap.Point(lng, lat);
				var gc = new BMap.Geocoder();
				gc.getLocation(point, function(rs) {
					var addComp = rs.addressComponents;
					mapArr.city = addComp.city;
				});
			},
			iploac(result){//根据IP设置地图中心
			    var cityName = result.name;
			   // map.setCenter(cityName);
			},
			onblur(){

			},
			onfocus(){

			}

        },
    }
</script>