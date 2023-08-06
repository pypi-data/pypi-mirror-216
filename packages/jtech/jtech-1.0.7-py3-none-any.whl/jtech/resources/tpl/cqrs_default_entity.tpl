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

import java.io.Serializable;
import java.util.UUID;

/**
* class {{ className  }}Entity 
* 
* @author {{ username  }}
*/
@Data
@Builder
@AllArgsConstructor
public class {{ className }}Entity implements Serializable {

    //@Id
    private UUID id;

    //Others parameters...

}
