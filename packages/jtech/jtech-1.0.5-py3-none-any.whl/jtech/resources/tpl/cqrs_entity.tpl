/*
 *  @(#){{ className }}Entity.java
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
package {{ package }}.entities;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.BeanUtils;

/**
* class {{ className  }}Entity 
* 
* user {{ username  }} 
*/
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {{ className }}Entity {

    //@NotEmpty(message = "ID not generated")
    //@Id
    private String id;

    //Others parameters...

    public static {{ className }} of({{ className }}Request request) {
        var entity = new {{ className }}();
        BeanUtils.copyProperties(request, entity);
        return entity;
    }

}
