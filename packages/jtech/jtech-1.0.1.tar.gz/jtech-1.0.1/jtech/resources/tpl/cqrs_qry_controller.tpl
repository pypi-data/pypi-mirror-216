
/*
*  @(#)Find{{className}}ByIdController.java
*
*  Copyright (c) J-Tech Solucoes em Informatica.
*  All Rights Reserved.
*
*  This software is the confidential and proprietary information of J-Tech.
*  ("Confidential Information"). You shall not disclose such Confidential
*  Information and shall use it only in accordance with the terms of the
*  license agreement you entered into with J-Tech.
*
*/
package {{ package }}.controllers.queries;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import {{ package }}.aggregate.{{ className }}Aggregate;

/**
* class Find{{ className }}ByIdController
* 
* user {{ username }}
*/
@RestController
@RequestMapping("/api/v1/{{ project }}s")
@RequiredArgsConstructor
public class Find{{ className }}ByIdController {

    private final {{ className }}Aggregate aggregate;

    @GetMapping("/{id}")
    public ResponseEntity<{{ className }}Response> findById(@PathVariable String id) {
        var response = aggregate.findById(new Find{{ className }}ByIdQuery(id));
        return ResponseEntity.ok(response);
     }
 }
