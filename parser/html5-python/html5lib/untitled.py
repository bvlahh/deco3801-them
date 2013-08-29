if token["name"] == 'html':
    self.parser.singular.append(token["name"])
    if self.parser.singular.count(token["name"]) > 1:
        self.parser.parseError("multiple-instance-singular-tag", 
            {"name": token["name"]})

2522
2548
1363
2694