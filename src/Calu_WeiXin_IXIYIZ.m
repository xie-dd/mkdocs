function [MoI,ZhiXin,MAll] = Calu_WeiXin_IXIYIZ(p,SPOINT,DOF_Node,Mgg,p_id_ori)
% ## param
% - MoI: 卫星相对自己质心轴转动惯量; 3*1
% - ZhiXin: 卫星形心坐标; 3*1
% - MAll: 卫星沿三个方向的质量; 3*1

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GID = p(end,:);
xyz = p(1:3,:);
SPID = SPOINT(1,:)';
IDMAX = max(max(SPID),max(GID));
GXYZ = zeros(IDMAX,3);
GXYZ(GID,:) = xyz';


SPDOF = SPID * 0;
for ii = 1:length(SPDOF)
    SPDOF(ii) = DOF_Node{SPID(ii)}(6);
end

Mgg_6 = diag(Mgg);
Mgg_6(SPDOF) = [];
errControl = max(max(abs(p(1,:))))/1E6;


disp = sqrt(p(2,:).^2+p(3,:).^2);
II = find(disp>errControl);
wxNodeID = p_id_ori(II);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 计算卫星质心
MXAll = 0;
MYAll = 0;
MZAll = 0;
ZhiXinX = 0;
ZhiXinY = 0;
ZhiXinZ = 0;

for ii = 1:length(wxNodeID)
    node_id = wxNodeID(ii);
    dof_x = DOF_Node{node_id}(1);
    mxi = Mgg_6(dof_x);
    MXAll = MXAll + mxi;
    MYAll = MYAll + Mgg_6(dof_x+1);
    MZAll = MZAll + Mgg_6(dof_x+2);

    xi = GXYZ(node_id,1);
    ZhiXinX = ZhiXinX + mxi * xi;
end

ZhiXinX = ZhiXinX/MXAll;
ZhiXin = [ZhiXinX;ZhiXinY;ZhiXinZ];
MAll = [MXAll;MYAll;MZAll];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 计算卫星质心


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 计算卫星相对自己质心轴转动惯量
MoI_X = 0;
MoI_Y = 0;
MoI_Z = 0;

for ii = 1:length(wxNodeID)
    node_id = wxNodeID(ii);
    dof_x = DOF_Node{node_id}(1);
    mxi = Mgg_6(dof_x);
    myi = Mgg_6(dof_x+1);
    mzi = Mgg_6(dof_x+2);

    xi = GXYZ(node_id,1);
    yi = GXYZ(node_id,2);
    zi = GXYZ(node_id,3);
    rx2i = (yi-ZhiXinY).^2 + (zi-ZhiXinY).^2;
    ry2i = (xi-ZhiXinX).^2 + (zi-ZhiXinZ).^2;
    rz2i = (xi-ZhiXinX).^2 + (yi-ZhiXinY).^2;
    MoI_X = MoI_X + mxi * rx2i;
    MoI_Y = MoI_Y + myi * ry2i;
    MoI_Z = MoI_Z + mzi * rz2i;
end
MoI = [MoI_X;MoI_Y;MoI_Z];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 计算卫星相对自己质心轴转动惯量






