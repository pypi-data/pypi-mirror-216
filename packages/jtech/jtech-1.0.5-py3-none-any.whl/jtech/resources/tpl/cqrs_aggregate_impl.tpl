/*
 *  @(#){{ className }}AggregateImpl.java
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
package {{ package }}.aggregate.impl;

import {{ package }}.aggregate.{{ className }}Aggregate;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * {{ className }}AggregateImpl
 *
 *  user {{ username }}
 */
@Service
@RequiredArgsConstructor
public class {{ className }}AggregateImpl implements {{ className }}Aggregate {

    private final Create{{ className }}Service createService;

    @Override
    public Optional<{{ className }}Entity> create({{ className }}Command command) {
        return createService.create(command.toEntity());
    }

}
