import rhinoscriptsyntax as rs
names = rs.AliasNames()
print names
for name in names:
    if 'RV' in name:
        rs.DeleteAlias(name)

