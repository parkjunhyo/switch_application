curl -X POST http://20.0.2.224:8088/net_builder/config_templates/1/ -d '[{"mgmt_swname":"CA5-E-KR1B-24-MG-03R05","mgmt_desc_uptor":"CA5-E-KR1B-24-L2-UP-03R05-Ma1","mgmt_desc_downtor":"CA5-E-KR1B-24-L2-DN-03R05-Ma1","mgmt_network":"10.11.24.0/24"}]' -H "Content-Type: application/json" -u root:password

curl -X DELETE http://20.0.2.224:8088/net_builder/mgmtsw_list/CA5-E-KR1B-24-MG-03R05/ -H "Content-Type: application/json" -u root:password
