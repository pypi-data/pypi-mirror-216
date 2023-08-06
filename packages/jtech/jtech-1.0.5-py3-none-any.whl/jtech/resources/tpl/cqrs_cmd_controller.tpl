
/*
*  @(#) Create{{className}}Controller.java
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
package {{ package }}.controllers.commands;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import {{ package }}.aggregate.*;
import {{ package }}.protocols.*;

import static {{ package }}.entities.{{ className }}.of;

/**
* class Create{{ className }}Controller
* 
* user {{ username }}
*/
@RestController
@RequestMapping("/api/v1/{{ project }}s")
@RequiredArgsConstructor
public class Create{{ className }}Controller {

    private final {{ className }}Aggregate aggregate;

    @PostMapping
    public ResponseEntity<{{ className }}Response> create(@RequestBody {{ className }}Request request) {
        var response = aggregate.create(of(request));
        return ResponseEntity.ok({{ className }}Response.of(response));
     }
 }
