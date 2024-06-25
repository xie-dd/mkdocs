function [MoI,ZhiXin,MAll] = Calu_WeiXin_IXIYIZ(p,SPOINT,DOF_Node,Mgg,p_id_ori)
% ## param
% - MoI: 卫星相对自己质心轴转动惯量; 3*1
% - ZhiXin: 卫星形心坐标; 3*1
% - MAll: 卫星沿三个方向的质量; 3*1
X = 0;

function [MoI,ZhiXin,MAll] = A2(p, ...
    SPOINT,DOF_Node, ...
    Mgg,p_id_ori)
% ## param
% - MoI: 卫星相对自己质心轴转动惯量; 3*1
% - ZhiXin: 卫星形心坐标; 3*1
% - MAll: 卫星沿三个方向的质量; 3*1
X = 1

function [MoI,ZhiXin,MAll] = A3(p, ...
    SPOINT, ...
    DOF_Node, ...
    Mgg,p_id_ori)
% ## param
% - MoI: 卫星相对自己质心轴转动惯量; 3*1
% - ZhiXin: 卫星形心坐标; 3*1
% - MAll: 卫星沿三个方向的质量; 3*1
X = 2